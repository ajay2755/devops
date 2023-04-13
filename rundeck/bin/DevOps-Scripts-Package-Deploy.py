import datetime
import requests
import string
import yaml
import shutil
import sys
import os
from zipfile import ZipFile

#Global variables
workspace = "python_workspace"
artifactory_api_key = ''

def get_config_values(input_item):
    #Open config files to read values based on keys.
    file_path = os.path.relpath("../config/config.yml")
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)['rundeck']
        return config[input_item]
        
def artifactory_file_download(filename):
    # Set request headers 
    headers = {'X-JFrog-Art-Api': artifactory_api_key}
    
    #Download file from artifactory
    response = requests.get( get_config_values('artifactory_path') + '/' + filename, headers=headers, verify=False)
    
    if response.status_code == 200:
        #Save file in local workspace 
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("Export Filename::",filename)
    else:
        print("Failed to download file from artifactory. Error code:", response.status_code)
        print(response.text)
              
def unzip_package(filename):
    #Unzip package
    with ZipFile(filename,"r") as zip_ref:
        zip_ref.extractall(workspace)

def cleanup_workspace():
    #Clean existing workspace 
    if os.path.exists(workspace):
        os.system('rm -rf '+ workspace)
    else:
        print('No directory for cleanup')
	
if __name__ == "__main__":
    
    if len(sys.argv) >= 3:
        artifactory_api_key = sys.argv[1]
        filename = sys.argv[2]
        cleanup_workspace()
        artifactory_file_download(filename)
        unzip_package(filename)
        os.remove(filename)
        print ("success:",len(sys.argv))
    else:
        example = 'python  DevOps-Scripts-Package-Deploy.py <artifactory_token> <git_token>'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')

	
