import requests
import yaml
import sys

def delete_user(username):
    """
    Delete user with username from Artifactory
    """
    
    with open("config.yml", "r") as stream:
        config = yaml.safe_load(stream)['artifactory']


    url = config['delete_user_url'].format(username=username)
    bearer_token = config['bearer_token']
    headers = {
        "Authorization": f"Bearer {bearer_token}",
    }

    # Send DELETE request
    response = requests.delete(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 204:
        print("Successfully deleted user from Artifactory.")
    else:
        print("Failed to delete user from Artifactory. Error code:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        username = sys.argv[1]
        delete_user(username)
    else:
        example = 'python ArtifactoryDeleteUser.py username'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')