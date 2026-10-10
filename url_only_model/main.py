from url_only_model.RFPhishingURLClassifier import RFPhishingURLClassifier

if __name__ == "__main__":
    # NOTE: This is an URL-only classifier. It does not fetch the page itself
    # Reference table:
    # true positive -> real phishing site
    # true negative -> real legitimate site
    # false positive -> legit site misclassified as phishing (annoying, too many alarms given to the user, but passable)
    # false negative -> phishing site misclassified as legit (dangerous, the user may be susceptible to attacks)
    # isHttps is a great label for eliminating about 20 false positives ()
    rf_phishing_model = RFPhishingURLClassifier()
    rf_phishing_model.train()

    # rf_phishing_model.predict_URL("<some whatever url>")

"""
    TRAIN RESULTS:
        Accuracy: 0.9976
        Recall:   0.9991
        F1:       0.9979
    The importance of each feature in model prediction
        IsHTTPS                       3.843669e-01   <- most important feature!
        NoOfOtherSpecialCharsInURL    1.666703e-01
        NoOfDegitsInURL               8.939761e-02
        DegitRatioInURL               8.483394e-02
        LetterRatioInURL              7.898492e-02
        SpacialCharRatioInURL         6.637585e-02
        NoOfLettersInURL              5.120085e-02
        NoOfSubDomain                 3.819409e-02
        DomainLength                  2.860064e-02
        TLDLength                     9.194254e-03
        NoOfQMarkInURL                1.512355e-03
        NoOfEqualsInURL               6.461848e-04
        NoOfAmpersandInURL            1.875296e-05
        IsDomainIP                    2.292433e-06
        ObfuscationRatio              4.877918e-07
        NoOfObfuscatedChar            4.186237e-07
        HasObfuscation                1.318598e-07   <- least important feature!
"""