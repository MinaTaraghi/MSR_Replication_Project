import pandas as pd

# this files aggregates the 17 dfs that were made in "pp_ratio_handler.py" and makes a unified dataset
# with both criteria values (c3 :commit frequency, and c2: puppet percentage) \
# inputs:
# repos_c2_p"+{part}+".csv" for part [0-16]
# "repos_all_c3_new.csv" that contains all the data for commit frequency, produced in main.py
# outputs:
# "repo_all_c2.csv" that contains the unified dataset for puppet percentage
# "c2_c3.csv" that contains both criteria for all the 235 Mirantis repositories / some that
# are forked have wrong values in this one
# "forked.csv" which has all the forked repos to be processed later
# "non-forked.csv" and "non_forked_criteria.csv" which contain all the non-forked repos and only the ones that
# meet both criteria 2 and 3 respectively



# aggrageting all the 17 parts together for c2
dfs = []
for i in range(0, 17):
    df_part = pd.read_csv("repos_c2_p"+str(i)+".csv")
    dfs.append(df_part)

df_all = pd.concat(dfs)
df_all.reset_index(inplace=True)
print(df_all.columns)
df_all= df_all[['name', 'c2', 'files', 'pp_files', 'forked']]
print(df_all)
df_all.to_csv("repo_all_c2.csv")
# reading dfs for c2 and c3
df_c3 = pd.read_csv("repos_all_c3_new.csv")
df_c2 = pd.read_csv("repo_all_c2.csv")


# merging dataframes for putting together all the data
result = pd.merge(df_c2, df_c3, on="name")
result = result[['name', 'c2', 'files', 'pp_files', 'forked',
       'c3', 'no_commits', 'month_diff', 'first_commit',
       'last_commit']]

result.to_csv("c2_c3.csv")
print(result.astype(bool).sum(axis=0))
print(result)

non_forked = result[result["forked"]==0]
non_forked.to_csv("forked.csv")
non_forked = non_forked.sort_values(by=["c2", "c3"], ascending= False)
print(non_forked)
non_forked.to_csv("non_forked.csv")

non_forked_criteria = non_forked[(non_forked["c2"]>=0.11) & (non_forked["c3"]>=2)]
non_forked_criteria.to_csv("non_forked_criteria.csv")