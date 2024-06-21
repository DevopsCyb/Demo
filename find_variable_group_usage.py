import requests
import os

# Azure DevOps organization and project details
organization = os.getenv('AZURE_DEVOPS_ORGANIZATION')
project = os.getenv('AZURE_DEVOPS_PROJECT')
base_url = f'https://dev.azure.com/{organization}/{project}/_apis'

# Personal Access Token (PAT) from environment variable
token = os.getenv('AZURE_DEVOPS_PAT')  # Ensure this token has appropriate permissions

# Endpoint to list pipelines
url = f"{base_url}/pipelines?api-version=6.0-preview.1"

headers = {
    'Authorization': f'Basic {token}',
    'Content-Type': 'application/json'
}

# Debug statements
print(f"Requesting URL: {url}")
print(f"Headers: {headers}")

# Send GET request to Azure DevOps REST API
response = requests.get(url, headers=headers)

# Check response status and handle accordingly
if response.status_code == 200:
    pipelines = response.json()['value']
    for pipeline in pipelines:
        pipeline_name = pipeline['name']
        print(f"Pipeline Name: {pipeline_name}")
else:
    print(f"Failed to retrieve pipelines. Status code: {response.status_code}")
    print(f"Response content: {response.text}")  # Print response content for further details
