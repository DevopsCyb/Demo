import requests
import base64
import os
import json

# Replace with your Azure DevOps organization URL, project name, and Personal Access Token (PAT)
organization = 'cybagedevops'
project = 'MIS'
personal_access_token = os.getenv('AZURE_DEVOPS_PAT')

# Base URL for Azure DevOps REST API
base_url = f'https://dev.azure.com/{organization}/{project}/_apis'

# Encode the PAT to base64 format
encoded_pat = base64.b64encode(f":{personal_access_token}".encode("utf-8")).decode("utf-8")

# Define headers and authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {encoded_pat}'
}

# Function to fetch pipeline details
def get_pipeline_details(pipeline_id):
    pipeline_url = f'{base_url}/pipelines/{pipeline_id}?api-version=6.0'
    response = requests.get(pipeline_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch pipeline details: {response.status_code} - {response.text}")
        return None

# Main script
if __name__ == "__main__":
    pipeline_id = '1301'  # Replace with your pipeline ID
    pipeline_details = get_pipeline_details(pipeline_id)
    if pipeline_details:
        # Print JSON formatted pipeline details
        print(json.dumps(pipeline_details, indent=2))
    else:
        print("Pipeline details not found.")
