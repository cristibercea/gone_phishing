from model.trainer import train_model
from model.tester import test_model
from features.extractor import extract_features_blk

TRAINING_DATASET = "./databases/training_dataset.csv"

TEST_DATASET =  "./databases/PhiUSIIL_Phishing_URL_Dataset.csv"


def gone_phising(model,url):
    selected_features = list(model.feature_names_in_)
    X = extract_features_blk([url], selected_features)
    
    prediction = model.predict(X)[0]
    probabillities = model.predict_proba(X)[0]
    print(f"Results for {url}")

    if prediction == 0:
        print("Possible Phissing")
    else:
        print("Possibly legit")
        
    print(f"Confidence: {max(probabillities) * 100}%")

if __name__ == "__main__":

    #Train model
    print("Training model")
    model = train_model(TRAINING_DATASET)

    #print testing
    print("Testing:")
    test_model(model,TEST_DATASET)


    #single url example
    gone_phising(model,"https://amazon.com")
    