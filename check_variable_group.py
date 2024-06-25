#!/usr/bin/env python

import requests
import os
import base64
import json

# Azure DevOps organization URL and PAT (Personal Access Token)
organization = os.getenv('AZURE_ORG')
project = os.getenv('AZURE_PROJECT')
pipeline_id =os.getenv('VARIABLE_GROUP_ID')
api_version = "7.1"
pat = os.getenv('AZURE_PAT')

# Construct the API URL
url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}?api-version={api_version}"

# Set headers and make the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {pat}"
}

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    pipeline_data = response.json()

    # Extract the names of variable groups
    if 'variables' in pipeline_data and 'variableGroups' in pipeline_data['variables']:
        variable_groups = pipeline_data['variables']['variableGroups']
        for group in variable_groups:
            print(group['name'])
    else:
        print("No variable groups found for this pipeline.")
else:
    print(f"Failed to fetch pipeline details. Status code: {response.status_code}")
