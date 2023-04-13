import sys
import requests
import yaml

def remove_user(username):
    """
    Remove user with username from Github organization
    
    """
    with open("config.yml", "r") as stream:
        config = yaml.safe_load(stream)['github']

    auth_token = config['auth_token']


    headers = {
        "Authorization": f"Token {auth_token}",
        "Accept": "application/vnd.github+json"
    }

    url = config['remove_from_org_url'].format(username=username)

    response = requests.delete(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 204:
        print("Successfully removed user from Github organization.")
    else:
        print("Failed to remove user from Github organization. Error code:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        username = sys.argv[1]
        remove_user(username)
    else:
        example = 'python GithubRemoveUserFromOrganization.py username'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
