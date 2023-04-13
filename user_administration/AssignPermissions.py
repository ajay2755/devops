import os
import sys
from sonarcloud_user import SonarcloudAddUserToGroup
from github_user import GithubInviteCollaboratorToRepo

def assign_permissions(sonargroup_user_file, github_user_file):
    """
    Using parameters specified in user_file, assign permissions to users.
    This includes adding a Sonarcloud user to an existing group and inviting collaborators to a repo.
    Each line in the SonarCloud user_file should specify one user like so:
    username group
    Each line in the Github user_file should specify one user like so:
    username user_role repo_name
    """
    script_path = os.path.dirname(os.path.realpath(__file__))

    if (sonargroup_user_file != ""):
        sonargroup_user_path = os.path.join(script_path, sonargroup_user_file)
        file = open(sonargroup_user_path, "r")
        for line in file:
            params = line.rstrip().split() 
            if len(params) != 2:
                raise Exception('Wrong number of arguments')
            
            username = params[0]
            sonar_group = params[1]

            SonarcloudAddUserToGroup.add_user_to_group(username, sonar_group)

        file.close()


    if (github_user_file != ""):
        github_user_path = os.path.join(script_path, github_user_file)
        file = open(github_user_path, "r")
        for line in file:
            params = line.rstrip().split() 
            if len(params) != 3:
                raise Exception('Wrong number of arguments')
            
            username = params[0]
            user_role = params[1]
            repo_name = params[2]

            GithubInviteCollaboratorToRepo.invite_collaborator(username, user_role, repo_name)
        
        file.close()

if __name__ == "__main__":
    example = 'python AssignPermissions.py s=sonargroup_user_file.txt g=github_user_file.txt'

    if len(sys.argv) == 2 or len(sys.argv) == 3:
        # Specify file containing users
        for i in sys.argv[1:]:
            if i.startswith("s="):
                assign_permissions(i[2:], "")
            elif i.startswith("g="):
                assign_permissions("", i[2:])
            else:
                raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
    else:
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
