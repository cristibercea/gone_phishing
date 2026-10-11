import pandas as pd
from config.features import SELECTED_FEATURES
from features.extractor import extract_features_blk

def build_dataset(input_file, output_file):
    # Load from the LegitPhish database and keep only the URL and Target labels
    df = pd.read_csv(input_file)
    df = df[["URL", "ClassLabel"]]
    df = df.dropna(subset = ["URL", "ClassLabel"]).reset_index(drop = True)
    
    
    # Extract URLs

    urls = df["URL"].tolist()

    # Create features df

    features_df = extract_features_blk(urls, SELECTED_FEATURES)

    # Create final dataset

    dataset = pd.concat([df[["URL"]], features_df, df[["ClassLabel"]]], axis = 1)

    dataset.to_csv(output_file, index = False)


if __name__ == "__main__":
    build_dataset(input_file="./databases/LegitPhish.csv", output_file = "./databases/training_dataset.csv")