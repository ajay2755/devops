rundeck
 |-bin
 | |-DevOps-Scripts-Package-Deploy.py [Parameters: <artifactory-api-key> <zip file name>    Desc: Deploy all devops scripts from artifactory to rundeck executor node]
 | |-DevOps-Scripts-Package-Upload.py [Parameters: <artifactory-api-key> <git-api-token>    Desc: Upload all devops repo scripts from git to artifactory]
 | |-Export-Rundeck-Jobs.py [Parameters: <artifactory_token> <rundeck_token> <projects> <git-token> <git-user> <rundeck-runid>    Desc: Export rundeck jobs and upload in artifactory]
 | |-Import-Rundeck-Jobs.py [Parameters: <artifactory_token> <rundeck_api_token> <zip_filename>    Desc: Download package from artifactory and import rundeck jobs]
 | |-Import-Rundeck-Policies.py [Parameters: <artifactory_token> <zip_filename> <env_type>    Desc: Download policy package from artifactory and import rundeck policies]
 |-config
 | |-config.yml [configurations for bin/ python scripts]
 | |-jaas-activedirectory.conf [Active Directory configurations]
 | |-resources.yaml [Node setup configurations]
 |-policies
 | |-rundeck_administrators.aclpolicy [Admin policy]
 | |-rundeck_read.aclpolicy [Read policy]
 | |-rundeck_read_execute.aclpolicy [Read and Execute policy]
 | |-rundeck_read_write_execute_create.aclpolicy [Read, Write, Create and Execute policy]
 |-readme.md 

#Rundeck policy groups for Active Directory (AD) - Non-Prod
rundeck_administrators
rundeck_read_write_execute_create
rundeck_read
rundeck_read_execute

#Rundeck policy groups for Active Directory (AD) - Production
prod_rundeck_administrators
prod_rundeck_read_write_execute_create
prod_rundeck_read
prod_rundeck_read_execute
