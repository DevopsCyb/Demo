import requests
import os
# Replace with your Azure DevOps organization URL and pipeline ID
org_url =  os.getenv('ORGANIZATION')
pipeline_id =  os.getenv('PIPELINE_ID')

# API endpoint to get pipeline details
url = f"{org_url}/_apis/pipelines/{pipeline_id}?api-version=6.0-preview.1"

# Replace with your Azure DevOps personal access token
token = os.getenv('PAT')

headers = {
    "Authorization": f"Basic {token}"
}

# Make GET request to fetch pipeline details
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    pipeline_data = response.json()
    
    # Example: Printing variables from pipeline data
    variables = pipeline_data.get("variables", {})
    for name, var_data in variables.items():
        value = var_data.get("value", "")
        is_secret = var_data.get("isSecret", False)
        print(f"Variable: {name}, Value: {value}, Secret: {is_secret}")
else:
    print(f"Failed to fetch pipeline details. Status code: {response.status_code}")

