import os
import subprocess
import pandas as pd

# this file gets the list of 21 selected mirantis repositories and 
# clones them in "/home/mina/Desktop/Puppet"
# and makes the file-XCM dataset for it
# input: "mirantis_messages.csv" mirantis messages
# inout: "mirantis_repos.csv" the list of 21 selected mirantis repos
# output: "mirantis_XCM_ds.csv" the file-xcm mirantis repo
df = pd.read_csv("mirantis_messages.csv")
# getting the list of repo names
repo_list = pd.read_csv("mirantis_repos.csv",header = None).values.tolist()
print(repo_list)
print(len(repo_list))
files_data = {}
for repo_ls in repo_list:
    repo = repo_ls[0]
    df_repo = df[df["repo"]==repo]
    print(df_repo)
    os.chdir(r"/home/mina/Desktop/Puppet")
    bashCommand = "pwd"
    #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    #output, error = process.communicate()
    print(subprocess.run(bashCommand))
    # cloning the repo
    bashCommand = ["git", "clone",  "https://github.com/Mirantis/"+repo+".git"]
    print(subprocess.run(bashCommand))
    # changing woring directory to repo
    os.chdir(repo)
    bashCommand = "pwd"
    print(subprocess.run(bashCommand))
    for row in df_repo.iterrows():   # for each commit
        sha = row[1]["commit"]
        message = row[1]["message"] 
        # get the list of affected files
        bashCommand = ["git", "diff-tree" ,"--no-commit-id" ,"--name-only" ,"-r" ,sha]
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
        output, error = process.communicate()
        strout = output.decode("utf-8")
        for s in strout.split("\n"):
            print(s)
            # adding commit message to the xcm of .pp files affected 
            if s.endswith(".pp"):
                if (s in files_data):
                    files_data[repo+ "/"+s] = files_data[repo+ "/"+s] + message
                else:
                    files_data[repo + "/"+s] = message

df_out = pd.DataFrame(list(files_data.items()))
# returning to base directory
os.chdir(r"/home/mina/Desktop/Puppet")
# string the output
df_out.to_csv("mirantis_XCM_ds.csv", header = ["file_", "XCM"])

