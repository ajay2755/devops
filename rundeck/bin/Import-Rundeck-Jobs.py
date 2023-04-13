import requests
import secrets
import string
import yaml
import sys
import os
import shutil
import time
from zipfile import ZipFile

#global variables
artifactory_api_key = ''
Rundeck_Auth_Token = ''
    
def get_config_values(input_item):
    #Open config files to read values based on keys.
    file_path = os.path.relpath("../config/config.yml")
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)['rundeck']
        return config[input_item]

def unzip_file(zip_filename):
    #Unzip file
    dir_name = zip_filename[0:-4]
    with ZipFile(zip_filename, 'r')  as zipObj:
        zipObj.extractall(path=dir_name)

    print("Unzip Directory created... - Directory name:",dir_name)    
 
def get_file_list(zip_filename):
    #Return file list from zip file
    with ZipFile(zip_filename, 'r')  as zipObj: 
        listOfiles = zipObj.namelist()
        return listOfiles

def get_project_name_from_file(filename):
    #Return project name from file name    
    x = filename.split("_export_")
    project_name = x[0]
    return project_name
 
def download_artifact(artifact_name):
    #Download artifact
    #Set request headers 
    headers = {'X-JFrog-Art-Api': artifactory_api_key} 
    
    #Download file from artifactory
    response = requests.get( get_config_values('artifactory_path') + '/' + artifact_name, headers=headers, verify=False) 
    
    if response.status_code == 200:
        #Save file in local workspace 
        with open(artifact_name, 'wb') as f:
            f.write(response.content)
        print("Export Filename::",artifact_name)
    else:
        print("Failed to download file from artifactory. Error code:", response.status_code)
        print(response.text)
                    
def get_project_info(project_name):
    #Set url from config
    url = get_config_values('prod_rundeck_url') + '/project/' + project_name
    
    #Set request headers
    headers = {
        "Accept": "application/json",
        "X-Rundeck-Auth-Token": Rundeck_Auth_Token
    }
    
    # Send GET request to check project info
    response = requests.get(url, headers=headers)
    
    #Return status code
    return response.status_code
    
        
def import_jobs(project_name,filename):
    #Set url from config
    url = get_config_values('prod_rundeck_url') + '/project/' + project_name + '/jobs/import?fileformat=yaml&uuidOption=remove&dupeOption=update'  
    
    #Set request headers
    headers = {
        "Accept": "application/json",
        "X-Rundeck-Auth-Token": Rundeck_Auth_Token,
        "Content-Type": "application/yaml"
    }

    # Send POST request
    data = open(filename, 'rb').read()
    response = requests.post(url, headers=headers, data=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Rundeck jobs successfully imported",response.text)
    else:
        print("Failed to import rundeck jobs. Error code:", response.status_code)
        print(response.text)
        exit()

def create_project(project_name):
    #Set url from config
    url = get_config_values('prod_rundeck_url') + '/projects'
    
    # Configure request url and headers
    headers = { 
    
        "Accept": "application/json",
        "X-Rundeck-Auth-Token": Rundeck_Auth_Token,
        "Content-Type": "application/json"
    }
    
    # Configure payload
    payload = {
        "name": project_name
    }
     
    # Send POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 201:
        print("Project_Name::",project_name)  
        print("Project Successfully created...",response.text)    
    else:
        print("Failed to create rundeck project. Error code:", response.status_code)
        print(response.text)
        exit()
          
if __name__ == "__main__":
    if len(sys.argv) >= 4:
        artifactory_api_key = sys.argv[1]
        Rundeck_Auth_Token = sys.argv[2]
        zip_filename = sys.argv[3]
        print("Artifact Name:",zip_filename)
        print("Downloading artifact from artifactory")
        download_artifact(zip_filename)
        print("Artifact downloaded successfully")
        
        unzip_file(zip_filename)
        print("Unzip Artifact in local path completed")
        
        print("Import process started")
        listOfiles = get_file_list(zip_filename)
        
        dir_name = zip_filename[0:-4]
        print("Directory Name::",dir_name)
        
        for elem in listOfiles:
            print("File Name::",elem)
            project_name = get_project_name_from_file(elem)
            print("Project Name::",project_name)
            status_code = get_project_info(project_name)
            
            if status_code == 200:
                print("Project found --> status code::",status_code)
                print("Import started")
                import_jobs(project_name,dir_name+'/'+elem)
                print("Import completed")
            else:
                print("Project not found --> status code::",status_code)
                print("Initiated create project request")
                create_project(project_name)
                print("Project created")
                print("Import started")
                import_jobs(project_name,dir_name+'/'+elem)
                print("Import completed")
                #os.close(elem)
        print("Import process completed")
        os.remove(zip_filename)
        shutil.rmtree(dir_name)
    else:
        example = 'python  Import-Rundeck-Jobs.py <artifactory_token> <git_token> <zip_filename>'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
        