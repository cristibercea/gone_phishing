from url_model.RFPhishingURLClassifier import RFPhishingURLClassifier

def training_menu(phishing_classifier: RFPhishingURLClassifier) -> None:
    """
    The user interface menu for training the phishing URL classifier.
    :param phishing_classifier: the phishing URL classifier.
    :return: None
    """
    print("\n/=======================| Gone_Phishing Training Menu |=======================\\")
    print("|   Commands:                                                                 |")
    print("|      train <path_to_PhiUSIIL_Phishing_URL_Dataset> - Trains URL Model       |")
    print("|               -> if not given a path, the default path used is:             |")
    print("|                      'databases/PhiUSIIL_Phishing_URL_Dataset.csv'          |")
    print("|      back - Back to Main Menu                                               |")
    print("\\=============================================================================/\n")

    while True:
        command = input(">> Insert command:\n>> ").split()
        if len(command) < 1 or len(command) > 2:
            print("\n[ERROR] Invalid command!")
            continue
        if command[0] == "back": break
        if command[0] == "train":
            try:
                if len(command) == 2:
                    phishing_classifier.train(command[1])
                else:
                    phishing_classifier.train()
            except FileNotFoundError as e:
                print("\n[ERROR] "+ e.__str__())
            continue
        print("[ERROR] Invalid command!")