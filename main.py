from interface.run import run

if __name__ == "__main__": run()

"""    
    TRAIN RESULTS:
        Accuracy: 0.9973
        Recall:   0.9988
        F1:       0.9976
    The importance of each feature in model prediction
        IsHTTPS                       0.391692
        NoOfDegitsInURL               0.131523
        DegitRatioInURL               0.129667
        LetterRatioInURL              0.114231
        NoOfLettersInURL              0.093652
        DomainLength                  0.077025
        NoOfSubDomain                 0.047925
        TLDLength                     0.007625
        NoOfQMarkInURL                0.003230
        NoOfEqualsInURL               0.001290
        NoOfOtherSpecialCharsInURL    0.000941
        SpacialCharRatioInURL         0.000915
        NoOfAmpersandInURL            0.000251
        NoOfObfuscatedChar            0.000011
        IsDomainIP                    0.000010
        ObfuscationRatio              0.000009
        HasObfuscation                0.000002

"""