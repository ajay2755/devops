import sys
import os
from artifactory_user import ArtifactoryDeleteUser
from github_user import GithubRemoveUserFromOrganization


def delete_users(user_file):
    """
    Delete users specified in user_file from Github org and Artifactory.
    Each line in user_file should specify one user like so:
    github_username artifactory_username
    """
    script_path = os.path.dirname(os.path.realpath(__file__))
    user_path = os.path.join(script_path, user_file)

    file = open(user_path, "r")

    for line in file:
        params = line.rstrip().split() 
        if len(params) != 2:
            raise Exception('Wrong number of arguments')
        
        github_username, artifactory_username = params
        delete_user(github_username, artifactory_username)

def delete_user(github_username, artifactory_username):
    """
    Delete github_username and artifactory_username user from Github org and Artifactory respectively
    """
    GithubRemoveUserFromOrganization.remove_user(github_username)
    ArtifactoryDeleteUser.delete_user(artifactory_username)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Specify file containing users
        user_file = sys.argv[1]
        delete_users(user_file)
    elif len(sys.argv) == 3: 
        # Specify parameters for one user directly
        _, github_username, artifactory_username = sys.argv
        delete_user(github_username, artifactory_username)
    else:
        example = 'python DeleteUsers.py user_file.txt \n' + 'python DeleteUsers.py github_username artifactory_username'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')


 