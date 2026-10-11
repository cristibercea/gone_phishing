from features.selector import FEATURE_LIST
import features.baseline_features
import features.url_features
import pandas as pd

'''
Given a list of selected features and a url
return dictionary feature_name:value
'''

def extract_features(url, selected_features):
    result = {}

    for feature_name in selected_features:
        feature_function = FEATURE_LIST[feature_name]
        result[feature_name] = feature_function(url)
    
    return result

'''
Bilk version calling on extract_features for a list of urls,
return dataframe
'''

def extract_features_blk(urls, selected_features):
    result = []

    for url in urls:
        result.append(extract_features(url, selected_features))
    
    return pd.DataFrame(result)