## Branch Name Convention
The following branch naming convention is assumed:

| Location | File Name | File Type| Parameter | Description |
|----------|-------------|-------------|-------------|-------------|
| devops/rundeck/bin | DevOps-Scripts-Package-Deploy.py | python script | <artifactory-api-key> <zip file name> | Deploy all devops scripts from artifactory to rundeck executor node |
| devops/rundeck/bin | DevOps-Scripts-Package-Upload.py | python script | <artifactory-api-key> <git-api-token> | Upload all devops repo scripts from git to artifactory |
| devops/rundeck/bin | Export-Rundeck-Jobs.py | python script | <artifactory_token> <rundeck_token> <projects> <git-token> <git-user> <rundeck-runid> | Export rundeck jobs and upload in artifactory |
| devops/rundeck/bin | Import-Rundeck-Jobs.py | python script | <artifactory_token> <rundeck_api_token> <zip_filename> | Download package from artifactory and import rundeck jobs |
| devops/rundeck/bin | Import-Rundeck-Policies.py | python script | <artifactory_token> <zip_filename> <env_type> | Download policy package from artifactory and import rundeck policies |
