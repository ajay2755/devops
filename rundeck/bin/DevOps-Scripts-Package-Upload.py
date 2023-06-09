import datetime
import requests
import string
import yaml
import shutil
import sys
import os
import glob
from zipfile import ZipFile

#Global variables
x = datetime.datetime.now()
date_time = x.strftime("%y%m%d%H%M%S")
zip_filename = 'devops_project_export_' + date_time + '.zip'
repo_name = "devops"
branch = 'master'
username = 'devops'
artifactory_api_key = ''
dir_name = 'devops_' + date_time

def get_config_values(input_item):
    #Open config files to read values based on keys.
    file_path = os.path.relpath("../config/config.yml")
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)['rundeck']
        return config[input_item]
        
def git_clone(git_token):
    #clone git devops repo in local workspace
    os.system('mkdir '+ dir_name)
    git_clone_url = get_config_values('git_clone_url')
    git_cmd = 'git -c http.sslVerify=false clone --single-branch --branch '+ branch +' https://'+ username +':'+ git_token +'@' + git_clone_url
    os.system('cd '+ dir_name +' && '+git_cmd)
    os.system('cd '+ dir_name +'/'+ repo_name + ' && rm -rf .git')
    
def artifactory_file_upload():
    #Upload package to artifactory
    with open(zip_filename, 'rb') as f:
        data = f.read()
    #Set headers
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8','X-JFrog-Art-Api': artifactory_api_key}
    #Send put request to upload package 
    response = requests.put(get_config_values('artifactory_path') +'/'+ zip_filename, headers=headers, data=data, verify=False)
   
    # Check if the request was successful
    if response.status_code == 201:
        print("File successfully uploaded::",response.status_code)
        print(response.text)
    else:
        clean_workspace()
        print("upload failed ::",response.status_code)
        raise Exception(response.text)
        
def create_package():
    #Create ZIP package for devops scrips
    with ZipFile(zip_filename, 'w') as zf:
        for dirname, subdirs, files in os.walk(dir_name+'/'+repo_name):
            x = dirname[19:]
            zf.write(dirname,x)
            for filename in files:
                zf.write(os.path.join(dirname, filename),os.path.join(x, filename))
                   
def clean_workspace():	
    #Clean/remove files and directories from local workspace
    if os.path.exists(dir_name):
        os.system('rm -rf '+ dir_name)
        
    if os.path.exists(zip_filename):
        os.system('rm -f '+ zip_filename)
        
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        artifactory_api_key = sys.argv[1]
        git_token = sys.argv[2]
        git_clone(git_token)
        create_package()
        artifactory_file_upload()
        clean_workspace()
    else:
        example = 'python  DevOps-Scripts-Package-Upload.py <artifactory_token> <git_token>'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
	
