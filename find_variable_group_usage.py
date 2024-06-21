import requests
from requests.auth import HTTPBasicAuth  # Basic authentication

# Replace with your Azure DevOps organization URL and project name
organization = 'cybagedevops'
project = 'MIS'

# Replace with your Personal Access Token (PAT)
personal_access_token = ''

# Base URL for Azure DevOps REST API
base_url = f'https://dev.azure.com/{organization}/{project}/_apis/pipelines'

# Define headers and authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {personal_access_token}'
}

# Function to fetch all pipelines
def get_all_pipelines():
    pipelines_url = f'{base_url}?api-version=6.0'
    response = requests.get(pipelines_url, headers=headers)

    if response.status_code == 200:
        pipelines_data = response.json()
        return pipelines_data['value']
    else:
        print(f"Failed to fetch pipelines: {response.status_code} - {response.text}")
        return []

# Function to print pipeline details
def print_pipeline_details(pipeline):
    print(f"Pipeline ID: {pipeline['id']}")
    print(f"Name: {pipeline['name']}")
    print(f"Description: {pipeline['description']}")
    print(f"URL: {pipeline['_links']['web']['href']}")
    print(f"Trigger Type: {pipeline['trigger']['type']}")
    print("Trigger Branch Filters:", pipeline['trigger']['branchFilters'])
    print("Variables:")
    for variable in pipeline['variables']:
        print(f"  {variable['name']}: {variable['value']}")
    print("Stages:")
    for stage in pipeline['stages']:
        print(f"  Stage Name: {stage['name']}")
        print("  Jobs:")
        for job in stage['jobs']:
            print(f"    Job Name: {job['name']}")
            print(f"    Status: {job['status']}")
            print(f"    Start Time: {job['startTime']}")
            print(f"    End Time: {job['endTime']}")
            print("    Tasks:")
            for task in job['tasks']:
                print(f"      Task Name: {task['name']}")
                print(f"      Status: {task['status']}")
                print(f"      Start Time: {task['startTime']}")
                print(f"      End Time: {task['endTime']}")
    print("")

# Main script
if __name__ == "__main__":
    pipelines = get_all_pipelines()
    for pipeline in pipelines:
        print_pipeline_details(pipeline)
