#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import os

# Fetch required values from environment variables
organization = os.getenv('AZURE_DEVOPS_ORGANIZATION')
project = os.getenv('AZURE_DEVOPS_PROJECT')
pat = os.getenv('AZURE_DEVOPS_PAT')
variable_group_name = os.getenv('VARIABLE_GROUP_NAME')

# Create a session with authentication
session = requests.Session()
session.auth = HTTPBasicAuth('', pat)

# Step 1: Get all pipelines
pipelines_url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines?api-version=6.0-preview.1"
pipelines_response = session.get(pipelines_url)
pipelines_response.raise_for_status()  # Raise an error for bad status codes
pipelines = pipelines_response.json().get('value', [])

# Initialize an empty list to store pipelines using the variable group
pipelines_using_variable_group = []

# Step 2: Get details for each pipeline
for pipeline in pipelines:
    pipeline_id = pipeline['id']
    pipeline_details_url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}?api-version=6.0-preview.1"
    pipeline_details_response = session.get(pipeline_details_url)
    pipeline_details_response.raise_for_status()  # Raise an error for bad status codes
    pipeline_details = pipeline_details_response.json()

    # Check if the variable group is used in the pipeline
    if 'variables' in pipeline_details:
        variables = pipeline_details['variables']
        if variable_group_name in variables:
            pipelines_using_variable_group.append(pipeline['name'])

# Print the list of pipelines using the variable group
print("Pipelines using the variable group:", pipelines_using_variable_group)
