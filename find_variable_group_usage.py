import requests
import os
import base64

# Fetch environment variables
organization = os.getenv('AZURE_DEVOPS_ORGANIZATION')
project = os.getenv('AZURE_DEVOPS_PROJECT')
pat = os.getenv('AZURE_DEVOPS_PAT')

# Check if environment variables are set
if not organization or not project or not pat:
    print("Environment variables AZURE_DEVOPS_ORGANIZATION, AZURE_DEVOPS_PROJECT, or AZURE_DEVOPS_PAT are not set.")
    exit(1)

# Base URL for Azure DevOps REST API
base_url = f'https://dev.azure.com/{organization}/{project}/_apis'

# Encode PAT for Basic Auth
encoded_pat = base64.b64encode(f':{pat}'.encode()).decode()

# Endpoint to list pipelines
url = f"{base_url}/pipelines?api-version=6.0-preview.1"

headers = {
    'Authorization': f'Basic {encoded_pat}',
    'Content-Type': 'application/json'
}

# Debugging: Print request details
print(f"Requesting URL: {url}")
print(f"Headers: {headers}")

# Send GET request to Azure DevOps REST API
response = requests.get(url, headers=headers)

# Check response status and handle accordingly
if response.status_code == 200:
    pipelines = response.json().get('value', [])
    if not pipelines:
        print("No pipelines found.")
    else:
        for pipeline in pipelines:
            pipeline_name = pipeline.get('name')
            print(f"Pipeline Name: {pipeline_name}")
else:
    print(f"Failed to retrieve pipelines. Status code: {response.status_code}")
    print(f"Response content: {response.text}")  # Print response content for further details
