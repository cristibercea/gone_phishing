import os, json, joblib, pandas as pd, seaborn as sns, matplotlib.pyplot as plt, numpy as np
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, f1_score, make_scorer
from sklearn.ensemble import RandomForestClassifier
from url_model.utils.features_extractor import extract_features
from url_model.utils.url_features import URL_FEATURES
from url_model.utils.validate_url import validate_url

class RFPhishingURLClassifier:
    """Prototype Random Forest Phishing URL Classifier"""

    def __init__(self, filename: str = 'PhiUSIIL_url_only_model.joblib') -> None:
        self.__clf = None
        self.__filename = filename
        try: self.load_from_file(filename)
        except FileNotFoundError: pass

    def get_model_store_filename(self) -> str | None:
        """
        Gets the filename of the model stored in models/ directory
        :return: the filename of the model stored in models/ directory or none if the path model/filename does not exist
        """
        return self.__filename if os.path.exists('models/'+self.__filename) else None

    def store_in_file(self, clf: RandomForestClassifier, filename: str = 'PhiUSIIL_url_only_model.joblib') -> None:
        """
        Save the trained model to a file, inside models/ directory.
        :param clf: the trained model
        :param filename: the name of the file
        :return: None
        """
        joblib.dump(clf, 'models/'+filename)

    def load_from_file(self, filename: str = 'PhiUSIIL_url_only_model.joblib') -> None:
        """
        Loads the model from a file located inside of models/ directory.
        :param filename: filename of the model
        :return: None
        :raises FileNotFoundError: if the file does not exist
        """
        if os.path.exists('models/'+filename):
            self.__filename = filename
            self.__clf = joblib.load('models/'+self.__filename)
            return
        raise FileNotFoundError(f'URL model file {filename} not found!')

    def train(self, dataset_filename: str = 'databases/PhiUSIIL_Phishing_URL_Dataset.csv') -> None:
        """
        Trains a RandomForestClassifier phishing URL model, on the dataset specified at dataset_filename, using URL_MODEL_FEATURES
        :param dataset_filename: path to the dataset CSV file
        :raises FileNotFoundError: if the database csv file does not exist
        :return: None
        """
        # FETCH DATASET
        if not os.path.exists(dataset_filename): raise FileNotFoundError(f'Dataset csv file \'{dataset_filename}\' not found!')
        PhiUSIIL = pd.read_csv(dataset_filename)

        # SELECT RELEVANT FEATURES
        subset = PhiUSIIL[URL_FEATURES + ['label', 'Domain']].dropna()
        X = subset[URL_FEATURES].values        # input:  URL metrics
        y = subset['label'].astype(int).values       # output: phishing/legit

        # GROUP INPUT DATA BY URL DOMAIN
        gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        train_idx, test_idx = next(gss.split(X, y, groups=subset['Domain'].values))
        """
        - grouping by registrable domain does not change the model's test performance
          (hosts are ~94% singletons, so this is closer to a random split than it looks).
        - we keep the group split because there is the stronger claim: no variant of any
          test domain appeared in training.
        """

        # TODO: maybe try recalculating the whole dataset features using extract_features and train again (if you cant solve extract_features function)
        # raw = pd.read_csv(dataset_filename)[['URL', 'label', 'Domain']].dropna(subset=['label'])
        # regen = pd.DataFrame([extract_features(u) for u in raw['URL']])
        # # Sanity: every training feature must exist in the extractor output
        # missing = set(URL_FEATURES) - set(regen.columns)
        # if missing:
        #     raise KeyError(f"extract_features is missing: {missing}")
        # X = regen[URL_FEATURES].values.astype(float)
        # y = raw['label'].astype(int).values
        # groups = raw['Domain'].values  # still group by registrable domain
        #
        # gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        # train_idx, test_idx = next(gss.split(X, y, groups=groups))

        # TRAINING & TEST DATA SPLIT
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # Tune the forest only on the training partition. GroupKFold keeps URLs
        # from the same domain together in each validation fold.
        param_grid = {
            # Broader search over forest size, tree complexity, feature
            # sampling, and class weighting; 108 combinations in total.
            'n_estimators': [150, 300, 450],
            'max_depth': [None, 20, 40],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 0.5],
            'class_weight': [None, 'balanced_subsample'],
        }
        cv = GroupKFold(n_splits=3)
        grid_search = GridSearchCV(
            # Parallelize across grid-search fits, not again inside each forest.
            estimator=RandomForestClassifier(n_jobs=1, random_state=42),
            param_grid=param_grid,
            # Dataset convention: 0 = phishing, 1 = legitimate.
            scoring=make_scorer(f1_score, pos_label=0),
            cv=cv,
            n_jobs=-1,
            refit=True,
            verbose=2,
        )
        grid_search.fit(X_train, y_train, groups=subset['Domain'].values[train_idx])
        self.__clf = grid_search.best_estimator_
        print(f"Best cross-validation F1: {grid_search.best_score_:.4f}")
        print(f"Best parameters: {grid_search.best_params_}")

        # SAVE MODEL STATE
        self.store_in_file(self.__clf, self.__filename)
        params_filename = os.path.splitext(self.__filename)[0] + '_training_info.json'
        with open(os.path.join('models', params_filename), 'w', encoding='utf-8') as info_file:
            json.dump({
                'best_params': grid_search.best_params_,
                'best_cv_f1_phishing': float(grid_search.best_score_),
                'scoring': 'F1, positive class 0 (phishing)',
                'cv': '3-fold GroupKFold grouped by Domain',
            }, info_file, indent=2)
            info_file.write('\n')
        print(f"Training details saved to: models/{params_filename}")

        # TEST
        y_pred = self.__clf.predict(X_test)

        # MEASURE
        imp = pd.Series(self.__clf.feature_importances_, index=URL_FEATURES).sort_values(ascending=False)
        conf_matrix = confusion_matrix(y_test, y_pred)

        # PRINT METRICS
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(f"Phishing recall: {recall_score(y_test, y_pred, pos_label=0):.4f}")
        print(f"Phishing F1:     {f1_score(y_test, y_pred, pos_label=0):.4f}")
        print("The importance of each feature in model prediction\n",imp)
        print("\n")
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', cbar=False, xticklabels=['Phishing', 'Legit'], yticklabels=['Phishing', 'Legit'])
        plt.title('Confusion Matrix Heatmap')
        plt.xlabel('Predicted Labels')
        plt.ylabel('True Labels')
        plt.show()

    def predict_URL(self, url: str) -> str:
        """
        Predict the URL using trained model.
        :param url: the URL to predict
        :return: "Phishing URL" if the URL is considered a phishing URL, "Legit URL" otherwise
        :raises AttributeError | : if the URL model is not loaded
        """
        if self.__clf is None: raise AttributeError('No URL model loaded!')
        validate_url(url)
        feats = extract_features(url)
        x = np.array([[feats[f] for f in URL_FEATURES]], dtype=float)
        proba = self.__clf.predict_proba(x)[0]
        phish_idx = int(np.where(self.__clf.classes_ == 0)[0][0])
        p_phish = float(proba[phish_idx])
        label = "Phishing URL!" if p_phish >= 0.5 else "Legit URL!"
        return f"{label} Probability: {p_phish:.3f}"


"""
# code to test our feature extraction function;
from extract_features import extract_features
sample = PhiUSIIL.sample(2000, random_state=0).copy()
    regen = pd.DataFrame([extract_features(u) for u in sample['URL']])

    for col in URL_MODEL_FEATURES:
        delta = (regen[col].values - sample[col].values)
        match = (np.abs(delta) < 1e-6).mean()
        print(f"{col:35s} match={match:.3f}  mean_delta={delta.mean():+.4f}")
    exit(0)
"""
