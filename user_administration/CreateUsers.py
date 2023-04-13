import os
import sys
from artifactory_user import ArtifactoryCreateUser
from github_user import GithubInviteUserToOrganization

def create_users(user_file):
    """
    Using parameters specified in user_file, create users in Artifactory and invite users to Github org
    Each line in user_file should specify one user like so:
    username github_role artifactory_password artifactory_grp
    """
    script_path = os.path.dirname(os.path.realpath(__file__))
    user_path = os.path.join(script_path, user_file)

    file = open(user_path, "r")

    for line in file:
        params = line.rstrip().split() 
        if len(params) < 3:
            raise Exception('Wrong number of arguments')
        
        username = params[0]
        github_role = params[1]
        artifactory_pwd = params[2]
        artifactory_grps = params[3:]

        create_user(username, github_role, artifactory_pwd, artifactory_grps)

def create_user(username, github_role, artifactory_grps):
    """
    Create a user with the specified parameters
    """
    GithubInviteUserToOrganization.invite_user(username, github_role)
    ArtifactoryCreateUser.create_user(username, artifactory_grps)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Specify file containing users' details
        user_file = sys.argv[1]
        create_users(user_file)
    elif len(sys.argv) >= 3:
        # Specify details for one user directly
        username = sys.argv[1]
        github_role = sys.argv[2]
        artifactory_grps = sys.argv[3:]
        create_user(username, github_role, artifactory_grps)
    else:
        example = 'python CreateUsers.py user_file.txt\n' + 'python CreateUsers.py username github_role artifactory_grp'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')

