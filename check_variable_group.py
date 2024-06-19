#!/usr/bin/env python

import os
import requests
from yaml import safe_load

# Azure DevOps organization and project
organization = os.getenv('AZURE_ORG')
project = os.getenv('AZURE_PROJECT')

# Personal Access Token
pat = os.getenv('AZURE_PAT')

# Headers for authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {pat}'
}

# Get all pipelines
pipelines_url = f'https://dev.azure.com/{organization}/{project}/_apis/pipelines?api-version=7.1-preview.1'
pipelines_response = requests.get(pipelines_url, headers=headers)
pipelines = pipelines_response.json()['value']

# Variable group to search for
variable_group_name = os.getenv('VARIABLE_GROUP_NAME')

# Function to check if variable group is used in YAML
def is_variable_group_used(yaml_content, variable_group_name):
    yaml_data = safe_load(yaml_content)
    variables = yaml_data.get('variables', [])
    for variable in variables:
        if 'group' in variable and variable['group'] == variable_group_name:
            return True
    return False

# List to store pipelines using the variable group
pipelines_using_variable_group = []

# Check each pipeline for the variable group usage
for pipeline in pipelines:
    pipeline_id = pipeline['id']
    yaml_url = f'https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}/yaml?api-version=7.1-preview.1'
    yaml_response = requests.get(yaml_url, headers=headers)
    yaml_content = yaml_response.text
    
    if is_variable_group_used(yaml_content, variable_group_name):
        pipelines_using_variable_group.append(pipeline)

# Output the pipelines using the variable group
if pipelines_using_variable_group:
    print("Pipelines using the variable group:")
    for pipeline in pipelines_using_variable_group:
        print(f"Pipeline ID: {pipeline['id']}, Name: {pipeline['name']}")
else:
    print("No pipelines found using the variable group.")
