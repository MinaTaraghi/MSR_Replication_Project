import pandas as pd
import requests
import time

# this file aggregates the XCMs and makes the file-XCM dataset for OpenStack Only
# function for processing the commit  updates the dictionary files_data and returns it
# inputs:
# expects to find file "OST.csv" for the authors' dataset of OpenStack.
# outputs :
# "openstack_messages.csv" that contains the dataset of file-XCM for OpenStack without labels
# "new_OST.csv" that contains the labels and file names (stripped of their local path prefix) for OpenStack
# "OST_labeled_XCM.csv" the final file-XCM dataset for our proposed classification problem

def commit_processor(row, orgname, files_data):
    repo = row["repo"]
    sha = row["commit"]
    if orgname == "openstack":
        response = requests.get(url = f"https://opendev.org/api/v1/repos/{orgname}/{repo}/git/commits/{sha}")
    commit_data = response.json()
    files = commit_data["files"]
    for file in files:
        if file["filename"].endswith(".pp"):
            filename = repo+"/"+file["filename"]
            if (filename in files_data):
                files_data[filename] = files_data[filename] + "\n" + row["message"]
            else:
                files_data[filename] = row["message"]


    return files_data

def file_XCM_aggregator(filename, orgname):

    #reading the file of
    df = pd.read_csv(filename, index_col=0)
    print(df)
    '''headers = {
        'Authorization': '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'
    }
    
    #
    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    print(response.text)
    print(response)'''
    files = set()
    files_data = {}

    for row in df.iterrows():
        dummy = commit_processor(row[1], orgname, files_data)

    print(files_data)
    df_out = pd.DataFrame(list(files_data.items()))
    df_out.to_csv(orgname+"_XCM_ds.csv")

    return df_out
if __name__ == '__main__':
    ds = file_XCM_aggregator("openstack_messages.csv", "openstack")
    #ds = pd.read_csv("openstack_XCM_ds.csv", index_col=0)
    ds.columns = ["file_", "XCM"]
    df_labels = pd.read_csv("OST.csv")
    print(df_labels.columns)

    #removing the prefix of the path of the authors' original data for each file
    df_labels["file_"] = df_labels["file_"].apply(lambda x: x[43:])
    # choosing only the file and the defect status
    df_labels = df_labels[["file_", "defect_status"]]
    df_labels.to_csv("new_OST.csv")
    # merging dataframes to get labels for all the files that we have collected that are present in their dataset
    labeled_XCM = ds.merge(df_labels, how="inner", on='file_')
    print(labeled_XCM)
    labeled_XCM.to_csv("OST_labeled_XCM.csv")