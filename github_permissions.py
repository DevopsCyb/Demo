import requests
import os

# Fetch GitHub token from environment variables
token = os.getenv('GITHUB_TOKEN')

# Headers for authentication
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# List of teams and their desired permissions
teams_permissions = {
    'CTG-Team': 'push',
   
    # Add more teams as needed
}

def list_repos(username):
    repos_url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(repos_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch repositories: {response.status_code} - {response.text}')
        return []

def update_team_permissions(repo_name, org, team_slug, permission):
    url = f'https://api.github.com/orgs/{org}/teams/{team_slug}/repos/{repo_name}'
    data = {
        'permission': permission
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 204:
        print(f'Updated {team_slug} permissions for {repo_name} to {permission}')
    else:
        print(f'Failed to update {team_slug} permissions for {repo_name}: {response.status_code} - {response.text}')

# Fetch organization and username from environment variables
org = os.getenv('GITHUB_ORG')
username = os.getenv('GITHUB_USERNAME')

# Fetch repositories and update permissions for each team
repos = list_repos(username)
for repo in repos:
    repo_name = repo['full_name']
    for team_slug, permission in teams_permissions.items():
        update_team_permissions(repo_name, org, team_slug, permission)
