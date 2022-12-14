from scipy.stats import mannwhitneyu
import pandas as pd
from cliffs_delta import cliffs_delta


# file that computes 2 out of 3 RQ1 requisites, i.e. Mann-Whitney U test and Cliff's Delta
# on 4 datasets and for 12 features
# inputs:
# expects to find the authors' dataset files as "MIR.csv", "MOZ.csv", "OST.csv", and "WIK.csv"
# ouputs:
# "{dataset_name}_MW.csv" and "{dataset_name}_cliff.csv" for each dataset
if __name__ == '__main__':
    #  reading the datasets from csv files
    mirantis = pd.read_csv("MIR.csv")
    mozilla = pd.read_csv("MOZ.csv")
    opens = pd.read_csv("OST.csv")
    wiki = pd.read_csv("WIK.csv")

    ds = [mirantis, mozilla, opens, wiki]
    columns = ['org', 'file_', 'URL', 'File', 'Lines_of_code', 'Require', 'Ensure',
               'Include', 'Attribute', 'Hard_coded_string', 'Comment', 'Command',
               'File_mode', 'SSH_KEY', 'defect_status']
    for df in ds:
        mw_org_dict = {}
        cd_org_dict = {}
        print(df.iloc[0]["org"])
        # separating defective and non-defective into two dataframes
        defective = df[df["defect_status"]==1]
        nondefect = df[df["defect_status"]==0]

        #iterating over features for computing the MWU-test
        for feature in columns[2:14]:
            feat_dict = {}
            cliff_dict = {}
            #separating the values of this feature for comparison
            fdf_d = defective[feature]
            fdf_nd = nondefect[feature]
            #performing Mann-Whitney U Test
            U1, p = mannwhitneyu(fdf_d,fdf_nd)
            print("Mann-Whitney Test Results for Feature "+ feature+":")
            print(feature)
            print(U1)
            print(p)
            print("-------------------------------")
            feat_dict["p"] = p
            feat_dict["p_round"] = round(p,4)
            feat_dict["U1"] = U1
            mw_org_dict[feature] = feat_dict
            # Going for Cliff's Delta
            d, res = cliffs_delta(fdf_d, fdf_nd)
            print("Cliff's Delta Results for Feature " + feature + ":")
            print(d, res)
            cliff_dict["delta"] = round(d, 3)
            cliff_dict["size"] = res
            cd_org_dict[feature] = cliff_dict
            print("***************************")
        print("###############################")
        # Saving the results' dataframe as CSV files
        out_df = pd.DataFrame.from_dict(mw_org_dict).T
        out_df.to_csv(df.iloc[0]["org"]+"_MW.csv")
        org_df = pd.DataFrame.from_dict(cd_org_dict).T
        org_df.to_csv(df.iloc[0]["org"] + "_cliff.csv")