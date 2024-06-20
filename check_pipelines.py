import requests
import os

# Retrieve environment variables
organization = os.getenv('AZURE_DEVOPS_ORGANIZATION')
project = os.getenv('AZURE_DEVOPS_PROJECT')
pat = os.getenv('AZURE_DEVOPS_PAT')
variable_group_id = os.getenv('VARIABLE_GROUP_ID')

# Base URL for Azure DevOps REST API
base_url = f'https://dev.azure.com/{organization}/{project}/_apis'

# Function to get all pipelines in the project
def get_all_pipelines():
    url = f'{base_url}/pipelines?api-version=6.0'
    response = requests.get(url, auth=('', pat))
    response.raise_for_status()
    return response.json()['value']

# Function to get the details of a pipeline
def get_pipeline_details(pipeline_id):
    url = f'{base_url}/pipelines/{pipeline_id}?api-version=6.0'
    response = requests.get(url, auth=('', pat))
    response.raise_for_status()
    return response.json()

# Function to check if a pipeline uses the specified variable group
def pipeline_uses_variable_group(pipeline):
    pipeline_id = pipeline['id']
    pipeline_details = get_pipeline_details(pipeline_id)
    
    # Check variable groups in the YAML definition
    # Here, we assume the YAML is stored in the 'yml' field of the response (this may vary)
    yaml_content = pipeline_details.get('yml')
    if yaml_content and f'variables:\n  - group: {variable_group_id}' in yaml_content:
        return True

    return False

# Main script
def main():
    pipelines = get_all_pipelines()
    pipelines_using_variable_group = []

    for pipeline in pipelines:
        if pipeline_uses_variable_group(pipeline):
            pipelines_using_variable_group.append(pipeline)

    print(f'Pipelines using variable group {variable_group_id}:')
    for pipeline in pipelines_using_variable_group:
        print(f"- Pipeline ID: {pipeline['id']}")

if __name__ == "__main__":
    main()

