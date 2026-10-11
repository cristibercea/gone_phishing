import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from model.trainer import train_model
from features.extractor import extract_features_blk



def test_model(model,test_dataset):

    df_external = pd.read_csv(test_dataset)
   
    # keep only url and label for testing
    df_external = df_external[["URL","label"]]

    # Missing values 

    df_external = df_external.dropna(subset=["URL","label"])

    #target 

    y_external = df_external["label"].astype(int)

    # extract feautes from model
    selected_features = list(model.feature_names_in_)
    # Extract URLs

    X_external = extract_features_blk(df_external["URL"],selected_features)

    # Predict:


    y_external_pred = model.predict(X_external)
    


    accuracy_external = accuracy_score(y_external, y_external_pred)

    classification_rep_external = classification_report(y_external, y_external_pred)

    con_matrix_external = confusion_matrix(y_external,y_external_pred)

   

    print("\n\n\nTesting on big dataset:")

    print(f"Accuracy: {accuracy_external:.4f}")
    print("\nClassification Report:\n", classification_rep_external)
    print("\nConfusion Matrix:\n", con_matrix_external)



if __name__ == "__main__":

    model = train_model("./databases/training_dataset.csv")

    results = test_model(model,"./databases/PhiUSIIL_Phishing_URL_Dataset.csv",)