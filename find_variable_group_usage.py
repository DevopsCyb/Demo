import requests
import os
import base64
import yaml

# Fetch environment variables
organization = cybagedevops
project = MIS
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
pipelines_url = f"{base_url}/pipelines?api-version=6.0-preview.1"

headers = {
    'Authorization': f'Basic {encoded_pat}',
    'Content-Type': 'application/json'
}

# Debugging: Print request details
print(f"Requesting URL: {pipelines_url}")
print(f"Headers: {headers}")

# Send GET request to Azure DevOps REST API to list pipelines
response = requests.get(pipelines_url, headers=headers)

def get_pipeline_variable_groups(pipeline_id):
    # URL to get pipeline definition YAML
    pipeline_def_url = f"{base_url}/pipelines/{pipeline_id}/yaml?api-version=6.0-preview.1"
    response = requests.get(pipeline_def_url, headers=headers)
    if response.status_code == 200:
        pipeline_yaml = response.text
        pipeline_dict = yaml.safe_load(pipeline_yaml)
        variable_groups = []
        if 'variables' in pipeline_dict:
            for var in pipeline_dict['variables']:
                if 'group' in var:
                    variable_groups.append(var['group'])
        return variable_groups
    return []

# Check response status and handle accordingly
if response.status_code == 200:
    pipelines = response.json().get('value', [])
    if not pipelines:
        print("No pipelines found.")
    else:
        for pipeline in pipelines:
            pipeline_id = pipeline.get('id')
            pipeline_name = pipeline.get('name')
            variable_groups = get_pipeline_variable_groups(pipeline_id)
            print(f"Pipeline Name: {pipeline_name}")
            if variable_groups:
                print(f"  Variable Groups: {', '.join(variable_groups)}")
            else:
                print("  No Variable Groups associated.")
else:
    print(f"Failed to retrieve pipelines. Status code: {response.status_code}")
    print(f"Response content: {response.text}")  # Print response content for further details
