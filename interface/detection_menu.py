from url_model.RFPhishingURLClassifier import RFPhishingURLClassifier

def detection_menu(phishing_classifier: RFPhishingURLClassifier) -> None:
    """
    The user interface menu for running the phishing URL classifier.
    :param phishing_classifier: the phishing URL classifier.
    :return: None
    """
    print("\n/======================| Gone_Phishing Prediction Menu |======================\\")
    print("|   Commands:                                                                 |")
    print("|      predict <URL_to_predict> - run URL prediction for the given URL        |")
    print("|      back - Back to Main Menu                                               |")
    print("\\=============================================================================/\n")

    while True:
        command = input(">> Insert command:\n>> ").split()
        if len(command) < 1 or len(command) > 2:
            print("\n[ERROR] Invalid command!")
            continue
        if command[0] == "back": break
        if command[0] == "predict":
            try:
                if len(command) == 2:
                    print("\n[INFO] " + phishing_classifier.predict_URL(command[1]) + '\n')
                    continue
            except AttributeError as e:
                print("\n[ERROR] " + e.__str__())
                continue
        print("[ERROR] Invalid command!")