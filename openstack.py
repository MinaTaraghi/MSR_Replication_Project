import requests
import pandas as pd

# This file computes criteria 2 for openstack
# inputs: Null
# outputs: "openstack_pp_percentage.csv" that contains the puppet file percentage for all OpenStack repositories

if __name__ == '__main__':

    repos = []
    orgs =[]
    '''
    # getting the list of all organizations that have repos hosted on Opendev
    url = f"https://opendev.org/api/v1/orgs?per_page=100&page=1"
    #getting the name of organizations on openDev
    data = requests.get(url).json()
    for org in data:
        new_org = {}
        new_org["name"] = org["username"]
        orgs.append(new_org)'''

    #getting the name of repositories for Openstack
    # the range is ((1,45) since we know OpenStack has 1305 repos
    for page in range(1,45):
        #getting the list of repos
        url = f"https://opendev.org/api/v1/orgs/openstack/repos?page={page}"
        data = requests.get(url).json()
        # iterate over all openstack repos
        for repo in data:
            new_repo = {}
            name = repo["name"]
            new_repo["name"] = name
            # getting the languages used in this repo in bytes
            url = f"https://opendev.org/api/v1/repos/openstack/{name}/languages"
            data = requests.get(url).json()
            all_files = 0
            pp_files = 0
            for key, value in data.items():
                all_files+=value
                if key == "Puppet":
                    pp_files+=value
            #print(name)
            pp_percentage = 0
            # calculating Puppet percentage in repo
            try:
                pp_percentage = round((pp_files / all_files), 2)
            except:
                print("zero files")
            #print(pp_percentage)
            new_repo["pp_percentage"] = pp_percentage
            repos.append(new_repo)
    df = pd.DataFrame(repos)
    # storing the puppet percentage
    df.to_csv("openstack_pp_percentage.csv")

    print(len(repos))