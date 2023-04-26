## Python Scripts
| Location | Script Name |  Parameters | Description |
|----------|-------------|-------------|-------------|
| devops/rundeck/bin | DevOps-Scripts-Package-Deploy.py | artifactory-api-key, zip-file-name | Deploy all devops scripts, configs and policies from artifactory to rundeck executor node |
| devops/rundeck/bin | DevOps-Scripts-Package-Upload.py | artifactory-api-key, git-api-token | Upload all devops repo scripts from git to artifactory |
| devops/rundeck/bin | Export-Rundeck-Jobs.py | artifactory-api-key, rundeck_token projects, git-token, git-user, rundeck-runid | Export non-prod rundeck jobs and upload in artifactory, It will create new branch and merge request for new export files in github |
| devops/rundeck/bin | Import-Rundeck-Jobs.py | artifactory-api-key, rundeck_api_token, zip_filename | Download non-prod rundeck package from artifactory and import in prod rundeck |
| devops/rundeck/bin | Import-Rundeck-Policies.py | artifactory-api-key, zip_filename, env_type | Download policy package from artifactory and import rundeck policies |

## Configuration files
| Location | File Name |  Description |
|----------|-------------|-------------|
| devops/rundeck/config | config.yml | Manage all python script configurations |
| devops/rundeck/config | jaas-activedirectory.conf | Active Directory configurations |
| devops/rundeck/config | resources.yaml | Rundeck node configurations |

#### All Rundeck export files will be stored in _devops/rundeck/job_exports/_ location

## Rundeck policies and groups for Active Directory (AD)

| Location | File Name | Non-Prod AD Groups |  Prod AD Groups  |
|----------|-------------|-------------|-------------|
| devops/rundeck/policies | rundeck_administrators.aclpolicy | rundeck_administrators | prod_rundeck_administrators |
| devops/rundeck/policies | rundeck_read.aclpolicy | rundeck_read | prod_rundeck_read |
| devops/rundeck/policies | rundeck_read_execute.aclpolicy | rundeck_read_execute | prod_rundeck_read_execute |
| devops/rundeck/policies | rundeck_read_write_execute_create.aclpolicy | rundeck_read_write_execute_create | prod_rundeck_read_write_execute_create |

