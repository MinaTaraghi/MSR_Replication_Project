import requests
import json
import pandas as pd

# This file outputs a dataset of commits and their messages for pp files for repos in
# OpenStack that meet all the criteria
# inputs: "openstack_final.csv" that contains all the 41 reps and their criteria data
# outputs: "openstack_messages.csv" that contains all the commit messages for commits that had changed .pp files
# for selected repos in OpenStack
# XCMs are later manually added to this file

# reading the repos data that met the criteria
df = pd.read_csv("openstack_final.csv")
df = df[["name", "pp_percentage", "c3"]]
# renaming column
df = df.rename(columns={'c3': 'commit_frequency'})

# getting all 41 repo names
repo_names = df["name"].tolist()
ds = []
for repo in repo_names:
    # url for requesting repo commits
    url = f"https://opendev.org/api/v1/repos/openstack/{repo}/commits"
    commits = requests.get(url).json()
    for commit in commits:
        # flag to check if the commit is changing a .pp file
        commit_has_pp = False
        files = commit["files"]
        for file in files:
            if file["filename"].endswith(".pp"):
                # commit changes a .pp file, set the flag to True and break out of the loop
                commit_has_pp = True
                break
        # only if the commit had changed any .pp files
        if commit_has_pp:
            new_dict={}
            # insert a row of repo name, commit SHA-1 and its message into the dataframe
            new_dict["repo"] = repo
            new_dict["commit"] = commit["sha"]
            message = commit["commit"]["message"]
            new_dict["message"] = message
            ds.append(new_dict)


df = pd.DataFrame(ds)

df.to_csv("openstack_messages.csv")

