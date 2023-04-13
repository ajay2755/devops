import requests
import yaml
import sys


def add_user_to_group(username, group):
    """
    Add existing user with username to existing Sonarcloud group
    """

    with open("config.yml", "r") as stream:
        config = yaml.safe_load(stream)['sonarcloud']


    # Configure request url and headers
    url = config['add_to_group_url']
    bearer_token = config['bearer_token']
    organization = config['organization']

    headers = {
        "Authorization": f"Bearer {bearer_token}",
    }

    # Configure payload  
    payload = {
    "login": f'{username}@github' ,
    "name": group,
    "organization": organization
    }

    # Send POST request
    response = requests.post(url, headers=headers, data=payload)

    # Check if the request was successful
    if response.status_code == 204:
        print("Successfully added User to group.")
    else:
        print("Failed to add User to group. Error code:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        username = sys.argv[1]
        group = sys.argv[2]
        add_user_to_group(username, group)
    else:
        add_user_to_group(1,2)
        example = 'python SonarcloudAddUserToGroup.py username group'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')