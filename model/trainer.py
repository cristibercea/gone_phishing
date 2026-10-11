import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def train_model(dataset, random_state = 42):
    df = pd.read_csv(dataset)
    #missing value
    df = df.dropna(subset=["ClassLabel"])

    #target
    y = df["ClassLabel"].astype(int)
    #features
    X = df.drop(columns=["ClassLabel","URL"])


    #classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=None, min_samples_leaf=1, max_features="sqrt", random_state=random_state, n_jobs=-1)
    rf_classifier.fit(X, y)


    return rf_classifier
