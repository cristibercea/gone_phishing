import os, joblib, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from url_only_model.model_features import extract_features, URL_MODEL_FEATURES


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

    def train(self, dataset_filename: str = '../databases/PhiUSIIL_Phishing_URL_Dataset.csv') -> None:
        """
        Trains a RandomForestClassifier phishing URL model, on the dataset specified at dataset_filename, using URL_MODEL_FEATURES
        :param dataset_filename: path to the dataset CSV file
        :return: None
        """
        # FETCH DATASET
        PhiUSIIL = pd.read_csv(dataset_filename)

        # SELECT RELEVANT FEATURES
        subset = PhiUSIIL[URL_MODEL_FEATURES + ['label', 'Domain']].dropna()
        X = subset[URL_MODEL_FEATURES].values        # input:  URL metrics
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

        # TRAINING & TEST DATA SPLIT
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # TRAIN
        self.__clf = (RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=42)
                      if self.__clf is None else
                      self.__clf).fit(X_train, y_train)

        # SAVE MODEL STATE
        self.store_in_file(self.__clf, self.__filename)

        # TEST
        self.load_from_file()      # test model loading
        y_pred = self.__clf.predict(X_test)

        # MEASURE
        imp = pd.Series(self.__clf.feature_importances_, index=URL_MODEL_FEATURES).sort_values(ascending=False)
        conf_matrix = confusion_matrix(y_test, y_pred)

        # PRINT METRICS
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(f"Recall:   {recall_score(y_test, y_pred):.4f}")
        print(f"F1:       {f1_score(y_test, y_pred):.4f}")
        print("The importance of each feature in model prediction\n",imp)
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
        :raises AttributeError: if the URL model is not loaded
        """
        if self.__clf is None: raise AttributeError('No URL model loaded!')
        url_features = extract_features(url)
        classification = self.__clf.predict(url_features)
        return "Phishing URL" if classification else "Legit URL"

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