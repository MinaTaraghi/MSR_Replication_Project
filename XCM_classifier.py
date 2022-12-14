import pandas as pd
import numpy as np
from collections import Counter
import text_preprocess
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

# file that performs the text classification experiments for our proposed RQ with the saame 6 binary classifiers
# (CART, KNN, LR, NB, RF, and SVM) that we used for RQ3 on the dataset we made in "file_XCM_aggregator.py"
# inputs:
# "OST_labeled_XCM.csv" and "MIR_labeled_XCM.csv" the two datasets that we built in the dataset construction step
# ouputs:
# "dataset.csv" that contains the concatenated dataset of Mirantis and OpenStack
# "results_"+{encoding}+".csv" where encoding should be set in the code to be "BOW" or "tf-idf" (variable encoding)
# it contains the ('precision', 'recall', 'f1', 'roc_auc') for our dataset
# that each contains median of a 10-fold cross-validation run
if __name__ == '__main__':
    df_ost = pd.read_csv("OST_labeled_XCM.csv", index_col= 0)

    df_mir = pd.read_csv("MIR_labeled_XCM.csv", index_col= 0)

    df = pd.concat([df_ost, df_mir]).reset_index(drop = True)

    df.to_csv("dataset.csv")
    corpus = text_preprocess.cleanup(df)
    min_freq = 5
    encoding = "BOW" # can also be alternatively set to tf-idf
    #encoding = "tf-idf"
    if encoding == "BOW":
        X, Y = text_preprocess.create_count_corpora(corpus, min_freq)
    else:
        X, Y = text_preprocess.create_tfidf_corpora(corpus, min_freq)
    unique, counts = np.unique(Y, return_counts=True)
    print(dict(zip(unique, counts)))
    counter = Counter(Y)
    print(counter)
    results = {}
    metrics = ["precision", "recall", "f1", "roc_auc"]
    for metric in metrics:
        metric_result = {}
        #################### SVM ###################
        print("******* SVM ****************")
        model = SVC(kernel = 'linear', C = 1,gamma='auto', probability=True)
        scores = cross_val_score(model, X, Y, cv=10, scoring=metric)
        print(np.median(scores))
        metric_result["SVM"] = round(np.median(scores), 3)
        #################### CART ###################
        print("******* CART ****************")
        model = tree.DecisionTreeClassifier()
        scores = cross_val_score(model, X, Y, cv=10, scoring=metric)
        print(np.median(scores))
        metric_result["CART"] = round(np.median(scores), 3)
        #################### KNN ###################
        print("******* KNN ****************")
        model = KNeighborsClassifier()
        scores = cross_val_score(model, X, Y, cv=10, scoring=metric)
        print(np.median(scores))
        metric_result["KNN"] = round(np.median(scores), 3)
        #################### LR ###################
        print("******* LR ****************")
        print(np.median(scores))
        model = LogisticRegression(solver='lbfgs')
        scores = cross_val_score(model, X, Y, cv=10, scoring=metric)
        metric_result["LR"] = round(np.median(scores), 3)
        #################### NB ###################
        print("******* NB ****************")
        model = GaussianNB()
        scores = cross_val_score(model, X, Y, cv=10, scoring=metric)
        print(np.median(scores))
        metric_result["NB"] = round(np.median(scores), 3)
        #################### RF ###################
        print("******* RF ****************")
        model = RandomForestClassifier()
        forest = RandomForestClassifier(random_state=0)
        forest.fit(X, Y)
        scores = cross_val_score(model, X, Y, cv=10, scoring=metric)
        print(np.median(scores))
        metric_result["RF"] = round(np.median(scores), 3)
        print("---------------------------------")
        results[metric] = metric_result
df_out = pd.DataFrame.from_dict(results)
df_out.to_csv("results_"+encoding+".csv")


