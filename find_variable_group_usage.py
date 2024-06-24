import requests
import base64

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

# Function to fetch latest run details for a pipeline
def get_latest_run_details(pipeline_id):
    runs_url = f'{base_url}/pipelines/{pipeline_id}/runs?api-version=6.0&$top=1&$orderby=createdDate desc'
    response = requests.get(runs_url, headers=headers)

    if response.status_code == 200:
        runs_data = response.json()
        if runs_data['count'] > 0:
            return runs_data['value'][0]
        else:
            return None
    else:
        print(f"Failed to fetch latest run details: {response.status_code} - {response.text}")
        return None

# Function to fetch stages details from the latest run
def get_run_stages(run_id):
    stages_url = f'{base_url}/build/builds/{run_id}/timeline?api-version=6.0'
    response = requests.get(stages_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch run stages: {response.status_code} - {response.text}")
        return None

# Main script
if __name__ == "__main__":
    pipeline_id = '12345'  # Replace with your pipeline ID
    pipeline_details = get_pipeline_details(pipeline_id)
    if pipeline_details:
        latest_run_details = get_latest_run_details(pipeline_id)
        if latest_run_details:
            stages_data = get_run_stages(latest_run_details['id'])

            pipeline_response = {
                "id": pipeline_details['id'],
                "name": pipeline_details['name'],
                "revision": pipeline_details['revision'],
                "description": pipeline_details.get('description', ''),
                "url": pipeline_details['_links']['web']['href'],
                "trigger": {
                    "type": pipeline_details.get('trigger', {}).get('type', ''),
                    "branchFilters": pipeline_details.get('trigger', {}).get('branchFilters', [])
                },
                "variables": [
                    {"name": var_name, "value": var_value['value']} 
                    for var_name, var_value in pipeline_details.get('variables', {}).items()
                ],
                "stages": [],
                "latestRun": {
                    "id": latest_run_details['id'],
                    "status": latest_run_details['result'],
                    "startTime": latest_run_details['startTime'],
                    "endTime": latest_run_details['finishTime'],
                    "url": latest_run_details['_links']['web']['href']
                },
                "repository": {
                    "type": pipeline_details.get('repository', {}).get('type', ''),
                    "name": pipeline_details.get('repository', {}).get('name', ''),
                    "branch": pipeline_details.get('repository', {}).get('defaultBranch', ''),
                    "url": pipeline_details.get('repository', {}).get('url', '')
                }
            }

            # Parse stages and jobs from timeline
            if stages_data:
                stages = {}
                for record in stages_data['records']:
                    if record['type'] == 'Stage':
                        stages[record['id']] = {
                            "name": record['name'],
                            "jobs": []
                        }
                    elif record['type'] == 'Job':
                        job = {
                            "name": record['name'],
                            "status": record['result'],
                            "startTime": record.get('startTime', None),
                            "endTime": record.get('finishTime', None),
                            "tasks": []
                        }
                        if record['parentId'] in stages:
                            stages[record['parentId']]['jobs'].append(job)
                    elif record['type'] == 'Task':
                        task = {
                            "name": record['name'],
                            "status": record['result'],
                            "startTime": record.get('startTime', None),
                            "endTime": record.get('finishTime', None)
                        }
                        for stage in stages.values():
                            for job in stage['jobs']:
                                if job['name'] == record['parentName']:
                                    job['tasks'].append(task)
                                    break

                pipeline_response["stages"] = list(stages.values())

            print(pipeline_response)
        else:
            print("No latest run details found.")
    else:
        print("Pipeline details not found.")
