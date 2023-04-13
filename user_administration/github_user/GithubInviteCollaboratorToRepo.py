import sys
import requests
import yaml

def invite_collaborator(username, user_role, repo_name):

    with open("config.yml", "r") as stream:
        config = yaml.safe_load(stream)['github']

    auth_token = config['auth_token']

    # Github API endpoint for adding a collaborator
    url = config['invite_to_repo_url'].format(repo_name=repo_name, username=username)

    # Replace with your Github API personal access token
    headers = {
        "Authorization": f"Token {auth_token}",
        "Accept": "application/vnd.github+json"
    }

    data = f'{{"permission": "{user_role}"}}'

    # Send the PUT request to add the collaborator
    response = requests.put(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 204:
        print(f"Successfully added user as a collaborator of {repo_name}.")
    else:
        print(f"Failed to add user as a collaborator of {repo_name}. Error code:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        _, username, user_role, repo_name = sys.argv
        invite_collaborator(username, user_role, repo_name)
    else:
        example = 'python GithubInviteCollboratorToRepo.py username user_role repo_name'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
