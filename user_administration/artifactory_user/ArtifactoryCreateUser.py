import requests
import secrets
import string
import yaml
import sys

def create_user(username, groups):
    '''
    Create an Artifactory user with the specified parameters.
    Password is generated automatically.
    '''

    with open("config.yml", "r") as stream:
        config = yaml.safe_load(stream)['artifactory']

    email = f'{username}@sparksystems.sg'

    # Configure request url and headers
    url = config['create_user_url']
    bearer_token = config['bearer_token']
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    password = generate_password()

    # Configure payload
    payload = {
        "username": username,
        "password": password,
        "email": email,
        "groups": groups,
        "admin": False,
        "profile_updatable": False,
        "internal_password_disabled": False,
        "disable_ui_access": False
    }

    # Send POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 201:
        passwords_store = config['passwords_store']
        with open(passwords_store, 'a+') as f:
            f.write(f'{username}  {email}  {password}\n')
        print("Successfully created user in Artifactory.")
    else:
        print("Failed to create user in Artifactory. Error code:", response.status_code)
        print(response.text)

def generate_password():
    password = secrets.choice(string.digits) + secrets.choice(string.punctuation) + secrets.token_urlsafe(20) + secrets.choice(string.punctuation)
    return  password

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        username = sys.argv[1]
        groups = sys.argv[2:]
        create_user(username, groups)
    else:
        example = 'python ArtifactoryCreateUser.py username group'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
