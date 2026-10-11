'''
Simple decorator used for creating a dictionary with feature_name and its respective function.
Used for testing model performance on different features
'''

FEATURE_LIST = {}

def select_feature(name):
    def decorator(func):
        FEATURE_LIST[name] = func
        return func
    return decorator

