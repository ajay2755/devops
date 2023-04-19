import datetime
import requests
import string
import yaml
import shutil
import sys
import os
from zipfile import ZipFile

#Global variables
x = datetime.datetime.now()
date_time = x.strftime("%y%m%d%H%M%S")
workspace = "python_workspace"
artifactory_api_key = ''

def get_config_values(input_item):
    #Open config files to read values based on keys.
    file_path = os.path.relpath("../config/config.yml")
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)['rundeck']
        return config[input_item]
        
def artifactory_file_download(filename):
    #Set request headers
    headers = {'X-JFrog-Art-Api': artifactory_api_key}
    #Send GET request
    response = requests.get( get_config_values('artifactory_path') + '/' + filename, headers=headers, verify=False)
    
    #Check response status and download package
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully... Filename:",filename)
    else:
        print("Failed to download file from artifactory. Error code:", response.status_code)
        raise Exception(response.text)
        
        
def unzip_package(filename):
    #unzip package for deployment
    with ZipFile(filename,"r") as zip_ref:
        zip_ref.extractall(workspace)

def cleanup_workspace():
    #Clean workspace
    print("workspace_name:",workspace)
    if os.path.exists(workspace):
        os.system('rm -rf '+ workspace)
    else:
        print('No directory for cleanup')
    
def deploy_rundeck_policies():
    #deploy acl policies in rundeck directory
    deploy_cmd = 'cp ./python_workspace/devops/rundeck/policies/*.aclpolicy /etc/rundeck'
    os.system(deploy_cmd)
        
def backup_policies():
    bkp_file = 'backup_policies_'+ date_time +'.tar.gz'
    bkp_cmd = 'cd /etc/rundeck && tar -zcvf '+ bkp_file +' *.aclpolicy'
    os.system(bkp_cmd)
    print("backup file name :",bkp_file)
    
def update_policies():
    update_policy_file('rundeck_administrators.aclpolicy','rundeck_administrators')
    update_policy_file('rundeck_read.aclpolicy','rundeck_read')
    update_policy_file('rundeck_read_execute.aclpolicy','rundeck_read_execute')
    update_policy_file('rundeck_read_write_execute_create.aclpolicy','rundeck_read_write_execute_create')

def update_policy_file(filename,groupname):
    file_path = os.path.relpath("./python_workspace/devops/rundeck/policies/" + filename )
    fin = open(file_path, "rt")
    data = fin.read()
    data = data.replace(groupname, 'prod_'+ groupname)
    fin.close()  
    fin = open(file_path, "wt")
    fin.write(data)
    fin.close()
    
if __name__ == "__main__":
    if len(sys.argv) >= 4:
        artifactory_api_key = sys.argv[1]
        filename = sys.argv[2]
        env_type = sys.argv[3]
        print("Taking backup of existing policies")
        backup_policies()
        print("Downloading artifact from artifactory")
        artifactory_file_download(filename)
        print("Artifact downloaded successfully")
        print("Unzip package")
        unzip_package(filename)
        print("Removed zip package file")
        os.remove(filename)
        if env_type == 'prod':
            print("Updated policy groups for prod")
            update_policies()
        
        print("deployed policy files to /etc/rundeck")
        deploy_rundeck_policies()
        cleanup_workspace() 
        print("Policis successfully deployed...")
    else:
        example = 'python  Import-Rundeck-policies.py <artifactory_token> <git_token> <zip_filename>'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
