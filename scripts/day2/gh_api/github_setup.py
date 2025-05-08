import csv
import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG = os.getenv("GITHUB_ORG")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def create_repo(repo_name, private):
    url = f"https://api.github.com/orgs/{ORG}/repos"
    data = {
        "name": repo_name,
        "private": private.lower() == "true"
    }
    r = requests.post(url, json=data, headers=HEADERS)
    if r.status_code == 201:
        print(f"✅ Repository '{repo_name}' created.")
    elif r.status_code == 422:
        print(f"⚠️ Repository '{repo_name}' already exists.")
    else:
        print(f"❌ Failed to create repo '{repo_name}': {r.text}")

def create_team(team_name):
    url = f"https://api.github.com/orgs/{ORG}/teams"
    data = { "name": team_name }
    r = requests.post(url, json=data, headers=HEADERS)
    if r.status_code == 201:
        print(f"✅ Team '{team_name}' created.")
    elif r.status_code == 422:
        print(f"⚠️ Team '{team_name}' may already exist.")
    else:
        print(f"❌ Failed to create team '{team_name}': {r.text}")

def add_team_repo_permission(team, repo, permission):
    url = f"https://api.github.com/orgs/{ORG}/teams/{team}/repos/{ORG}/{repo}"
    data = { "permission": permission }
    r = requests.put(url, json=data, headers=HEADERS)
    if r.status_code in (204, 201):
        print(f"✅ Team '{team}' granted '{permission}' on '{repo}'.")
    else:
        print(f"❌ Failed to set permissions: {r.text}")

def add_user_to_team(team, username):
    url = f"https://api.github.com/orgs/{ORG}/teams/{team}/memberships/{username}"
    r = requests.put(url, headers=HEADERS)
    if r.status_code in (200, 201):
        print(f"✅ User '{username}' added to team '{team}'.")
    else:
        print(f"❌ Failed to add user '{username}' to team '{team}': {r.text}")

def load_repos(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def load_teams(path):
    teams = {}
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            team = row[0]
            users = [u.strip() for u in row[1:] if u.strip()]
            teams[team] = users
    return teams

def main():
    repos = load_repos("repos.csv")
    teams = load_teams("teams.csv")

    # Step 1 & 2: Create repos and teams
    for team_name in teams:
        create_team(team_name)

    for repo in repos:
        create_repo(repo['name'], repo['private'])
        add_team_repo_permission(repo['team'], repo['name'], repo['permission'])

    # Step 3: Assign users to teams
    for team, users in teams.items():
        for user in users:
            add_user_to_team(team, user)

if __name__ == "__main__":
    main()
