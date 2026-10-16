from url_model.RFPhishingURLClassifier import RFPhishingURLClassifier
from interface.main_menu import main_menu

def run() -> None:
    """
    NOTE: This is an URL-only classifier. It does not fetch the page itself
    Reference table:
    true positive -> real phishing site
    true negative -> real legitimate site
    false positive -> legit site misclassified as phishing (annoying, too many alarms given to the user, but passable)
    false negative -> phishing site misclassified as legit (dangerous, the user may be susceptible to attacks)
    :return: None
    """
    rf_phishing_model = RFPhishingURLClassifier()
    while main_menu(rf_phishing_model): pass