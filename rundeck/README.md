## Python Scripts
| Location | Script Name |  Parameter | Description |
|----------|-------------|-------------|-------------|
| devops/rundeck/bin | DevOps-Scripts-Package-Deploy.py | artifactory-api-key, zip-file-name | Deploy all devops scripts from artifactory to rundeck executor node |
| devops/rundeck/bin | DevOps-Scripts-Package-Upload.py | artifactory-api-key, git-api-token | Upload all devops repo scripts from git to artifactory |
| devops/rundeck/bin | Export-Rundeck-Jobs.py | artifactory-api-key rundeck_token projects git-token git-user rundeck-runid | Export rundeck jobs and upload in artifactory |
| devops/rundeck/bin | Import-Rundeck-Jobs.py | artifactory-api-key rundeck_api_token zip_filename | Download package from artifactory and import rundeck jobs |
| devops/rundeck/bin | Import-Rundeck-Policies.py | artifactory-api-key zip_filename env_type | Download policy package from artifactory and import rundeck policies |

## Configuration files
| Location | File Name |  Description |
|----------|-------------|-------------|
| devops/rundeck/config | config.yml | Manage all python script configurations |
| devops/rundeck/config | jaas-activedirectory.conf | Active Directory configurations |
| devops/rundeck/config | resources.yaml | Rundeck node configurations |
