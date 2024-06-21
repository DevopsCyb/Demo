#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import os

# Fetch required values from environment variables
organization = os.getenv('AZURE_DEVOPS_ORGANIZATION')
project = os.getenv('AZURE_DEVOPS_PROJECT')
pat = os.getenv('AZURE_DEVOPS_PAT')

# Create a session with authentication
session = requests.Session()
session.auth = HTTPBasicAuth('', pat)

# Step 1: Get all pipelines
pipelines_url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines?api-version=7.1-preview.1"
pipelines_response = session.get(pipelines_url)
pipelines_response.raise_for_status()  # Raise an error for bad status codes
pipelines = pipelines_response.json().get('value', [])

# Step 2: Print details for each pipeline
for pipeline in pipelines:
    pipeline_id = pipeline['id']
    pipeline_name = pipeline['name']
    repository_type = pipeline['repository']['type']
    repository_name = pipeline['repository']['name']
    pipeline_url = pipeline['_links']['web']['href']

    print(f"Pipeline ID: {pipeline_id}")
    print(f"Name: {pipeline_name}")
    print(f"Repository Type: {repository_type}")
    print(f"Repository Name: {repository_name}")
    print(f"Pipeline URL: {pipeline_url}")
    print("-" * 30)

# Optionally, you can perform further actions with these pipelines if needed.
