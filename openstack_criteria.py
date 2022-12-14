import requests
import pandas as pd
from urllib.parse import parse_qs, urlparse
from dateutil import parser, relativedelta

# This file computes criteria 3 (commit frequency) for openstack and combines it with
# puppet percentage from "openstack.py" to make the final OpenStack dataset
# inputs: "openstack_pp_percentage.csv" that contains the puppet file percentage for all OpenStack repositories
# outputs: "openstack_c2_c3.csv" that contains the final results for openstack for criteria 2 and 3

# Three repos just the same as mirantis in "main.py"
def time_diff(first, last):
    diff = relativedelta.relativedelta(last, first)
    return (diff.months + (12 * diff.years) + 1)

def parse_date(response):
    date = response["commit"]["committer"]["date"]
    p = parser.parse(date)
    return p.date()

def get_commits_count_date(owner_name, repo_name):
    # Returns the number of commits and their time period to a GitHub repository.

    url = f"https://opendev.org/api/v1/repos/{owner_name}/{repo_name}/commits"
    r = requests.get(url)
    last_commit_date = 0
    first_commit_date = 0
    diff = 0
    try:
        last_commit_date = parse_date(r.json()[0])
    except:
        print("^^^^^^ No 'last' date.")
        print(r.text)
        last_commit_date = 0
    links = r.links
    if len(r.json()) <= 30:
        first_commit_date = parse_date((r.json()[-1]))
        commits_count = len(r.json())
        diff = time_diff(first_commit_date, last_commit_date)
    try:
        rel_last_link_url = urlparse(links["last"]["url"])
        last = requests.get(links["last"]["url"]).json()
        rel_last_link_url_args = parse_qs(rel_last_link_url.query)
        rel_last_link_url_page_arg = rel_last_link_url_args["page"][0]

        commits_count = (int(rel_last_link_url_page_arg) - 1)*30 + len(last)
        try:
            first_commit_date = parse_date(last[-1])
            #print(last[-1])
            diff = time_diff(first_commit_date, last_commit_date)
        except:
            print("^^^^^^ No first date.")
            first_commit_date = 0

    except:
        print("^^^^^^ No 'last' link for ", repo_name)
    return commits_count, diff, first_commit_date, last_commit_date


if __name__ == '__main__':
    c2 = pd.read_csv("openstack_pp_percentage.csv",index_col=[0])
    new_rows = []
    for index , row in c2.iterrows():
        name = row["name"]
        # getting required data to compute commit frequency
        cc, diff, fcd, lcd =get_commits_count_date("openstack",name)
        # calculating commit frequency
        commit_frequency = round((cc/diff),2)
        '''print(name)
        print(commit_frequency)
        print("cc: ",cc)
        print("diff: ",diff)
        print("first: ", fcd)
        print("last: ", lcd)
        print("******************")'''
        row["c3"] = commit_frequency
        new_rows.append(row)
    new_df = pd.DataFrame(new_rows)
    # outputting the file
    new_df.to_csv("openstack_c2_c3.csv")