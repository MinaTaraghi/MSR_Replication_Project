from main import get_pp_percentage
import pandas as pd
import requests
import json

# This file computes criteria 2 for Mirantis datasets in batches of 14
# inputs: "repos_all_c3_new.csv"
# outputs:
# with each run it outputs f"repos_c2_p{part}.csv" that contains puppet files percentage for each file
# and also a column that indicates whether the repository is a forked one (to be later processed) or not

# getting the list of all repos for Mirantis that we got when we calculated commit frequency
df = pd.read_csv("repos_all_c3_new.csv")
names = list(df["name"])
print(names)
print(len(names))
 # this shoulkd be set from 1 to 16 in each run
# We could have put it in a loop but since it threw a bunch of various errors on different runs
# and we were doing this just once we decided to get and store each batch separately
# and set it manually for each run
part = 16
# index of repository to be mined in the list of repos
index = part*14

headers = {
        'Authorization': 'token #your token here#'
    }
# always checking the GitHub API rate limit since it is such a pain in the side :/
response = requests.get('https://api.github.com/rate_limit', headers=headers)
print(response.text)
repos = []
for i in range(index, index+14):
    name = names[i]
    ppp, files, pp_files, forked = get_pp_percentage(headers, "mirantis", name)
    print(name)
    print(round(ppp,4))
    print(files)
    print(pp_files)
    print(forked)
    repo_dict={}
    repo_dict["name"] = name
    repo_dict["c2"] = round(ppp,4)
    repo_dict["files"] = files
    repo_dict["pp_files"] = pp_files
    repo_dict["forked"] = forked
    repos.append(repo_dict)
    print("---------------------")
df = pd.DataFrame(repos)
print(df)
df.to_csv(f"repos_c2_p{part}.csv")
