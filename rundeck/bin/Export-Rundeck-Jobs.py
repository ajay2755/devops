import datetime
import requests
import secrets
import string
import yaml
import sys
import os
from zipfile import ZipFile


#Global variables
x = datetime.datetime.now()
date_time = x.strftime("%y%m%d%H%M%S")
zip_filename = 'rundeck_project_export_' + date_time + '.zip'
artifactory_api_key = ''
Rundeck_Auth_Token = ''

def get_config_values(input_item):
    #Open config files to read values based on keys.
    file_path = os.path.relpath("../config/config.yml")
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)['rundeck']
        return config[input_item]
        
def load_request_parameters():
    # Get configuration value from config.yml
    config_url = get_config_values('nonprod_rundeck_url')
    #set request headers
    headers = {
            "Accept": "application/json",
            "X-Rundeck-Auth-Token": Rundeck_Auth_Token,
            "Content-Type": "application/json"
        }
    return config_url,headers
            
def export_jobs(project_name):
    config_url,headers = load_request_parameters()
    url = config_url + '/project/' + project_name + '/jobs/export?format=yaml'
    # Send POST request to create export from rundeck
    response = requests.post(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        output_store = project_name + '_export_' + date_time + '.yaml'
        with open(output_store, 'a+') as f:
            f.write(f'{response.text}')
        print("Export Filename::",output_store)
        return output_store
    else:
        print("Failed to create rundeck export file. Error code:", response.status_code)
        print(response.text)

def artifactory_file_upload():
    
    with open(zip_filename, 'rb') as f:
        data = f.read()
    #Set headers
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8','X-JFrog-Art-Api': artifactory_api_key}
    #Send put request
    response = requests.put(get_config_values('artifactory_path') +'/'+ zip_filename, headers=headers, data=data, verify=False)
    
    if response.status_code == 201:
        print("File successfully uploaded::",response.status_code)
        print(response.text)
    else:
        print("upload failed ::",response.status_code)
        print(response.text)

def project_backups():
    config_url,headers = load_request_parameters()
    print("config_url -->", config_url)
    print("headers -->", headers)
    url = config_url + '/projects'

    # Send GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful and execute below steps
    if response.status_code == 200:
        content = response.json();
        
        #Get Rundeck project list to export jobs and create zip file
        with ZipFile(zip_filename, 'w') as f:
            for item in content:
                filename = export_jobs(item['name'])
                f.write(filename)
                os.remove(filename)
    else:
        print("Failed to create rundeck export file. Error code:", response.status_code)
        print(response.text)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        artifactory_api_key = sys.argv[1]
        Rundeck_Auth_Token = sys.argv[2]
        if len(sys.argv) >= 4:
            #Export jobs for selected project
            project_name = sys.argv[3]
            print("project name found, will export jobs for given project::",project_name)
            print ("Project Name::",project_name)
            filename = export_jobs(project_name)
            with ZipFile(zip_filename, 'w') as f:
                f.write(filename)
                os.remove(filename)
            artifactory_file_upload()
            print ("Zip file Name::",zip_filename)
            os.remove(zip_filename)
        else:
            #Export jobs for all projects
            print("Creating full dump for all projects")
            project_backups() 
            artifactory_file_upload()
            print("zip_filename::",zip_filename)
            os.remove(zip_filename)
    else:
        example = 'python  Export-Rundeck-Jobs.py <artifactory_token> <git_token>'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')