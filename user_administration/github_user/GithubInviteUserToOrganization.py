import sys
import requests
import yaml

def invite_user(username, user_role):
    """
    Invite a user to Github organization
    """

    with open("config.yml", "r") as stream:
        config = yaml.safe_load(stream)['github']

    auth_token = config['auth_token']

    # Github API endpoint for inviting users to an organization
    url = config['invite_to_org_url']

    # Replace with your Github API personal access token
    headers = {
        "Authorization": f"Token {auth_token}",
        "Accept": "application/vnd.github+json"
    }

    # Replace with the username of the user you want to invite
    user_email = f'{username}@sparksystems.sg'
    data = f'{{"email": "{user_email}", "role": "{user_role}"}}'

    # Send the POST request to the API endpoint
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 201:
        print("Successfully invited user to Github organization.")
    else:
        print("Failed to invite user to Github organization. Error code:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        username = sys.argv[1]
        user_role = sys.argv[2]
        invite_user(username, user_role)
    else:
        example = 'python GithubInviteUsertoOrganization username user_role'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
