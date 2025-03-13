import requests
import os
from config import GITHUB_TOKEN, GITHUB_USERNAME

BASE_URL = "https://api.github.com"
GITHUB_USERNAME = "ashishkr010"  
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 
BASE_URL = "https://api.github.com"


def create_github_repo(repo_name, private=True):
    
    url = f"{BASE_URL}/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"name": repo_name, "private": private}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully!")
    else:
        print(f"Failed to create repo: {response.json()}")




def create_pull_request(repo_name, branch_name, base_branch="main"):
    """Create a pull request on GitHub"""
    url = f"{BASE_URL}/repos/your_github_username/{repo_name}/pulls"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "title": f"Merge {branch_name} into {base_branch}",
        "head": branch_name,
        "base": base_branch,
        "body": f"Automated PR: Merging `{branch_name}` into `{base_branch}`"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Pull Request Created: {response.json()['html_url']}")
    else:
        print(f"Failed to create PR: {response.json()}")




"""
def create_github_pr(repo_name, branch_name, title="Merging feature branch"):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("ERROR: GitHub token not found!")
        return False

    api_url = f"https://api.github.com/repos/ashishkr010/{repo_name}/pulls"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    #feature -> target
    data = {
        "title": title,
        "head": branch_name,
        "base": "main",  
        "body": f"Automated PR to merge {branch_name} into main"
    }

    print(f"Debug: Sending PR request to {api_url}")
    print(f"Debug: Headers = {headers}")
    print(f"Debug: Payload = {data}")

    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 201:
        print("Pull request created successfully!")
        return True
    else:
        print(f"Failed to create PR: {response.json()}")
        return False
"""