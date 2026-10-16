from interface.detection_menu import detection_menu
from interface.training_menu import training_menu
from url_model.RFPhishingURLClassifier import RFPhishingURLClassifier

def main_menu(phishing_classifier: RFPhishingURLClassifier) -> bool:
    """
    The main menu of the Gone_Phishing app
    :param phishing_classifier:
    :return: True if the app should continue execution, False otherwise
    """
    print("\n\n/======================| Gone_Phishing |======================\\")
    print("|   Commands:                                                 |")
    print("|        train - Train Model                                  |")
    print("|        predict - Classify URL                               |")
    print("|        exit - Exit Gone_Phishing                            |")
    print("\\=============================================================/\n")
    match input(">> Insert command:\n>> "):
        case "train":
            training_menu(phishing_classifier)
        case "predict":
            detection_menu(phishing_classifier)
        case "exit":
            return False
        case _:
            print("[ERROR] Invalid command!")
    return True