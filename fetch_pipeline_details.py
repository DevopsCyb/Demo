import os
import requests

# Define variables from environment variables
organization = os.getenv('ORGANIZATION')
project = os.getenv('PROJECT')
pipeline_id = os.getenv('PIPELINE_ID')
pat = os.getenv('PAT')

# Set up the request URL and headers
url = f'https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}?api-version=6.0'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {pat}'
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check response status and print details
if response.status_code == 200:
    pipeline_details = response.json()
    print(pipeline_details)
else:
    print(f'Error: {response.status_code}')
    print(response.text)
