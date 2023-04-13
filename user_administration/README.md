# User Administration

## Directory Structure
```
.
├── artifactory_user          
│   ├── ArtifactoryCreateUser.py                 
│   └── ArtifactoryDeleteUser.py
├── github_user
│   ├── GithubInviteCollaboratorToRepo.py
│   ├── GithubInviteUserToOrganization.py
│   └── GithubRemoveUserFromOrganization.py
├── sonarcloud_user
│   └── SonarcloudAddUserToGroup.py
├── __init__.py
├── AssignPermissions.py
├── config.yml           # To be created by user
├── CreateUsers.py
├── DeleteUsers.py
├── README.md
└── requirements.txt
```

## Prerequisites

1. Install Python dependencies

   ``pip install -r requirements.txt``

2. Create a config file under ``user_administration/`` called `config.yml` with the following structure:

```
sonarcloud:
  add_to_group_url: <sonarcloud api url for adding user to group>
  bearer_token: <bearer token for authentication>
  organization: <sonarcloud organization name>

artifactory:
  create_user_url: <artifactory api url for creating user>
  delete_user_url: <artifactory api url for deleting user>
  bearer_token: <bearer token for authentication>
  passwords_store: <file name for storing generated passwords>

github:
  invite_to_org_url: <github api url for inviting user to org>
  invite_to_repo_url: <github api url for inviting collaborator to repo>
  remove_from_org_url: <github api url for removing user from org>
  organization: <github organization name>
```

  An example config file ``example-config.yml`` can be found in the ``user_administration/`` directory. 

## ArtifactoryCreateUser.py   
  
Create a user in Artifactory. A password is generated automatically and saved to the ``passwords_store`` file set in ``config.yml``.

``python ArtifactoryCreateUser.py username group``

## ArtifactoryDeleteUser.py 

Delete a user in Artifactory. 

``python ArtifactoryDeleteUser.py username``

## GithubInviteCollaboratorToRepo.py

Invite a collaborator to a Github repo.

``python GithubInviteCollboratorToRepo.py username user_role repo_name``


## GithubInviteUserToOrganization.py

Invite a user to the Github organization

``python GithubInviteUsertoOrganization username user_role``

## GithubRemoveUserFromOrganization.py

Remove a user from the Github organization

``python GithubRemoveUserFromOrganization.py username``

## SonarcloudAddUserToGroup.py

Add a user to existing Sonarcloud group

``python SonarcloudAddUserToGroup.py username group``

## AssignPermissions.py

Invite collaborators to Github repositories and assign SonarCloud users to specific groups. User, repository, permission and sonargroup details have to be specified through a file. For SonarCloud, add the ```s=``` prefix before the filename. For Github, add the ```g=``` prefix before the filename. For each file, use the following format to specify the relevant user/groups:

Sonarcloud:
```
username1 sonar_group1
username2 sonar_group2
``` 
Github:
```
username1 user_role1 repo_name1
username2 user_role2 repo_name2
```

``python AssignPermissions.py s=sonargrup_user_file.txt g=github_user_file``

## CreateUsers.py

Create users on Artifactory and invite users to the Github organization. User details can be specified through a file or through cli directly. If a file is used, multiple users can be added, and each line in the file should represent one user like so:

    username1 github_role1 artifactory_grp1
    username2 github_role2 artifactory_grp3

``python CreateUsers.py user_file.txt``

``python CreateUsers.py username github_role artifactory_grp``

## DeleteUsers.py

Delete users from Artifactory and the Github organization. User details can be specified through a file or through cli directly. If a file is used, multiple users can be deleted, and each line in the file should represent one user like so:

    github_username1 artifactory_username1
    github_username2 artifactory_username2

``python DeleteUsers.py user_file.txt``

``python DeleteUsers.py github_username artifactory_username``