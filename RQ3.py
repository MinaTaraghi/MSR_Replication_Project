import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.svm import SVC

# file that computes RQ3 requisites, i.e. log transformation, PCA , and 5 original classifiers
# (CART, KNN, LR, NB, RF) on 4 datasets
# also computes the classification results for one extra classifier "Support Vector Machine" or "SVM"
# also computes the feature importance for RQ1
# inputs:
# expects to find the authors' dataset files as "MIR.csv", "MOZ.csv", "OST.csv", and "WIK.csv"
# ouputs:
# "{metric_name}_median.csv" for four metrics ('precision', 'recall', 'f1', 'roc_auc')
# that each contains median of 10-fold cross-validation results for the all datasets

if __name__ == '__main__':
    mirantis = pd.read_csv("MIR.csv")
    mozilla = pd.read_csv("MOZ.csv")
    opens = pd.read_csv("OST.csv")
    wiki = pd.read_csv("WIK.csv")
    ds = [mirantis, mozilla, opens, wiki]
    columns = ['org', 'file_', 'URL', 'File', 'Lines_of_code', 'Require', 'Ensure',
       'Include', 'Attribute', 'Hard_coded_string', 'Comment', 'Command',
       'File_mode', 'SSH_KEY', 'defect_status']

    # We have computed the PCAs with the code below and calculated the number of minimum PCs that cover 95% of variance.
    # we are therefore merely giving them the number of PCs here in a list to be used
    pcas = [6,8,7,7]
    index = 0
    metrics = ['precision', 'recall', 'f1', 'roc_auc']
    for metric in metrics:
        results = {}
        for df in ds:
            print(df.iloc[0]["org"])
            org_dict = {}
            y = df[columns[-1]]
            # log transformation
            df_log = df[columns[2:14]].apply(lambda x: np.log(x+1))
            # PCA transformation (dimensionality reduction)
            pca = PCA(n_components= pcas[index])
            df_pca= pca.fit_transform(df_log)
            ################# PCA Calculation ########################
            #this piece of code was originally used to carry out PCA and get the variance ratios of PCs
            #pca = PCA(n_components='mle', svd_solver='full')
            #pca.fit(df_log)
            #print(pca.explained_variance_ratio_)
            #print("..............................")
            #pcas.append(pca.explained_variance_ratio_)
            # we then performed the variance cover anakysis manually as it was presented in our presentation

            #################### SVD ###################
            print("******* SVD ****************")
            model = SVC(kernel = 'linear', C = 1,gamma='auto', probability=True)
            scores = cross_val_score(model, df_pca, y, cv=10, scoring='roc_auc')
            print(np.median(scores))
            org_dict["CART"] = round(np.median(scores), 3)
        
            #################### CART ###################
            print("******* CART ****************")
            model = tree.DecisionTreeClassifier()
            scores = cross_val_score(model, df_pca, y, cv=10, scoring='precision')
            print(np.median(scores))
            org_dict["CART"] = round(np.median(scores), 3)
            #################### KNN ###################
            print("******* KNN ****************")
            model = KNeighborsClassifier()
            scores = cross_val_score(model, df_pca, y, cv=10, scoring='precision')
            print(np.median(scores))
            org_dict["KNN"] = round(np.median(scores), 3)
            #################### LR ###################
            print("******* LR ****************")
            print(np.median(scores))
            model = LogisticRegression(solver='lbfgs')
            scores = cross_val_score(model, df_pca, y, cv=10, scoring='precision')
            org_dict["LR"] = round(np.median(scores), 3)
            #################### NB ###################
            print("******* NB ****************")
            model = GaussianNB()
            scores = cross_val_score(model, df_pca, y, cv=10, scoring='precision')
            print(np.median(scores))
            org_dict["NB"] = round(np.median(scores), 3)
            #################### RF ###################
            print("******* RF ****************")
            #print(np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0))
            scores = cross_val_score(model, df_pca, y, cv=10, scoring='precision')
            print(np.median(scores))
            org_dict["RF"] = round(np.median(scores), 3)
            results[df.iloc[0]["org"]] = org_dict
            print("---------------------------------")
            #################### FI ###################
            model = RandomForestClassifier()
            forest = RandomForestClassifier(random_state=0)
            forest.fit(df_log, y)
            print(forest.feature_importances_)

            index += 1

        df_out = pd.DataFrame.from_dict(results).T
        df_out.to_csv(metric+"_median.csv")
