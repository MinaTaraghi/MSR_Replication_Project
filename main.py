import requests
import pandas as pd
from urllib.parse import parse_qs, urlparse
from dateutil import parser, relativedelta



# This file computes criteria 3 for Mirantis
# inputs: Null
# outputs: "repos_all_c3.csv" that contains the commit frequency for all Mirantis repos

def time_diff(first, last):
    # returns the time difference in months between two commit dates
    diff = relativedelta.relativedelta(last, first)
    return (diff.months + (12 * diff.years) + 1)

def parse_date(response):
    # returns the tmedate object of a commit (in a json response)
    date = response[0]["commit"]["committer"]["date"]
    p = parser.parse(date)
    return p.date()

def get_commits_count_date(headers, owner_name, repo_name):
    # Returns the number of commits to a GitHub repository.
    # also returns the last and first commit dates and the months difference between them
    url = f"https://api.github.com/repos/{owner_name}/{repo_name}/commits?per_page=1"
    r = requests.get(url,headers=headers)
    last_commit_date = 0
    first_commit_date = 0
    try:
        last_commit_date = parse_date(r.json())
    except:
        print("^^^^^^ No 'last' date.")
        print(r.text)
        last_commit_date = 0
    links = r.links

    try:
        rel_last_link_url = urlparse(links["last"]["url"])
        rel_last_link_url_args = parse_qs(rel_last_link_url.query)
        rel_last_link_url_page_arg = rel_last_link_url_args["page"][0]
        commits_count = int(rel_last_link_url_page_arg)

        url = links["last"]["url"]
        r = requests.get(url, headers=headers)
        try:
            first_commit_date = parse_date(r.json())
            diff = time_diff(first_commit_date, last_commit_date)
        except:
            print("^^^^^^ No first date.")
            first_commit_date = 0

    except:
        commits_count = 0
        diff = 1
        print("^^^^^^ No 'last' link.")
        print(repo_name, "is empty")
    return commits_count, diff, first_commit_date, last_commit_date


def get_pp_percentage(headers, owner_name, repo_name):
    forked = 0
    # getting the number of all files in the repo
    url = f"https://api.github.com/search/code?q=*+repo:{owner_name}/{repo_name}+fork:true"
    repo_data = requests.get(url, headers=headers).json()
    try:
        no_files = repo_data["total_count"]
    except:
        print(repo_data)
        print(repo_name)

    # getting the number of puppet files in the repo
    url = f"https://api.github.com/search/code?q=*+extension:.pp+repo:{owner_name}/{repo_name}"
    repo_data = requests.get(url, headers=headers).json()
    try:
        no_pp_files = repo_data["total_count"]
    except:
        print(repo_data)
        print(repo_name)
    # getting the percentage of puppet files in the repo
    try:
        IaC_percentage = no_pp_files / no_files
    except:
        print("^^^ could not get the number of files ***")
        IaC_percentage = 0
        forked = 1

    return IaC_percentage, no_files, no_pp_files, forked


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    headers = {
        'Authorization': 'token #your token here# }'
    }
    # checking the GitHub API rate limit
    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    print(response.text)
    print(response)
    # since we know Mirantis has 235 repositories (3 papers in total to be fetched if per_page is set to 100
    repos = []
    for page in range(1,4):
        url = f"https://api.github.com/orgs/mirantis/repos?type=all&per_page=100&page={page}"
        # make the request and return the json
        data = requests.get(url, headers=headers).json()
        for repo in data:
            name = (repo["name"])
            # getting required data to compute C3 or Commit Frequency
            no_commits, diff, first_date, last_date = get_commits_count_date(headers, "mirantis", name)
            print(name)
            print(no_commits)
            print(diff)
            #saving them in a dictionary
            repo_dict = {}
            repo_dict["name"] = name
            repo_dict["c3"] = round(no_commits/diff, 2)
            repo_dict["no_commits"] = no_commits
            repo_dict["month_diff"] = diff
            repo_dict["first_commit"] = first_date
            repo_dict["last_commit"] = last_date
            repos.append(repo_dict)
    df = pd.DataFrame(repos)
    print(df)
    #outputs the Commit frequency for all Mirantis Repos
    df.to_csv("repos_all_c3.csv")


