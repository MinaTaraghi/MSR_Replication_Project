import pandas as pd


# this file label the files from the mirantis file-XCM dataset for which 
# labels are available in the original datasets
# input: "mirantis_XCM_ds.csv" that contains the file-XCM dataset for Mirantis
# input: "MIR.csv" that is the paper's original dataset for Mirantis 
# output: "MIR_labeled_CXM.csv" that contains the labelled rows of the input for which label was available
# output: "new_MIR.csv" all the file names and their labels

# reading the file-XCM dataset
ds = pd.read_csv("mirantis_XCM_ds.csv", index_col=0)
ds.columns = ["file_", "XCM"]

# reading the original dataset
df_labels = pd.read_csv("MIR.csv")
print(df_labels.columns)
# removing the path prefix of the authors
df_labels["file_"] = df_labels["file_"].apply(lambda x: x[43:])

# extracting only the file names and their labels
df_labels = df_labels[["file_", "defect_status"]]
# storing labeled names
df_labels.to_csv("new_MIR.csv")

# merging the datasets
labeled_XCM = ds.merge(df_labels, how="inner", on='file_')

# outputting the new dataset
print(labeled_XCM)
labeled_XCM.to_csv("MIR_labeled_CXM.csv")
