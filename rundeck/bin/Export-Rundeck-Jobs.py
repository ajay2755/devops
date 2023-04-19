import datetime
import requests
import secrets
import string
import yaml
import sys
import os
import git
from zipfile import ZipFile

#Global variables
x = datetime.datetime.now()
date_time = x.strftime("%y%m%d%H%M%S")
year = x.strftime("%Y")
zip_filename = 'rundeck_project_export_' + date_time + '.zip'
artifactory_api_key = ''
Rundeck_Auth_Token = ''
filenames = [] 
branch_name = ''

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
        #output_store = project_name + '_export_' + date_time + '.yaml'
        output_store = project_name + '_export.yaml'
        with open(output_store, 'a+') as f:
            f.write(f'{response.text}')
        print("Export Filename::",output_store)
        return output_store
    else:
        #Clean workspace if failed and raise exception
        cleanup_workspace()
        print("Failed to create rundeck export file. Error code:", response.status_code)
        raise Exception(response.text)

def artifactory_file_upload():
    #Upload zip file in artifactory
    with open(zip_filename, 'rb') as f:
        data = f.read()
    #Set headers
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8','X-JFrog-Art-Api': artifactory_api_key}
    #Send put request
    response = requests.put(get_config_values('artifactory_path') +'/'+ zip_filename, headers=headers, data=data, verify=False)
    #Check response status
    if response.status_code == 201:
        print("File successfully uploaded::",response.status_code)
    else:
        #Clean workspace if failed and raise exception
        cleanup_workspace() 
        print("upload failed ::",response.status_code)
        raise Exception(response.text)

def git_add(filenames,git_user,git_token,run_id):
    # Get configuration value from config.yml
    config_url = get_config_values('git_clone_url')
    repo_clone_url = 'https://' + git_user + ':' + git_token + '@' + config_url
    #Repository name
    local_repo = "devops"
    #Set commit message
    msg = "Committed rundeck project export files for branch" + branch_name
    print('Creating new branch for export files')
    os.environ['GIT_SSL_NO_VERIFY'] = "1"
    #Clone repository in local workspace
    repo = git.Repo.clone_from(repo_clone_url, local_repo)
    
    #Create branch
    repo.git.checkout('-b', branch_name)
    
    #Add new files in git repo
    os.system('cd ./devops/rundeck && mkdir job_exports')
    os.system('mv *.yaml ./devops/rundeck/job_exports')
    repo.git.add([filenames])
    
    #Git Commit
    commit = repo.index.commit('Committed rundeck project export files for branch')
    #Git push
    repo.git.push('--set-upstream', 'origin', branch_name)
    
    print('Branch successfully created...')
    print('New branch name is :',branch_name)
        
def create_pull_request(git_token):
    #Set title & body
    title = 'Added/Updated rundeck job export files in ' + branch_name + ' branch'
    body = 'Please review and approve this changes'
    #Set url
    url = get_config_values('git_merge_url')
    #Set headers
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+ git_token,
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    #Set request body
    data = '{"title":"'+ title +'","body":"'+ body +'","head":"'+ branch_name +'","base":"master"}'
    #Send post request
    response = requests.post(url, headers=headers, data=data)
    #Check request status
    if response.status_code == 201:
        print('Merge request created successfully...',response.status_code)
    else:
        #Clean workspace if failed and raise exception
        cleanup_workspace() 
        print('Failed to create merge request',response.status_code)
        raise Exception(response.text)

def cleanup_workspace():
    os.system('rm -rf devops')
    os.system('rm -f *.yaml *.zip')
    
if __name__ == "__main__":
    if len(sys.argv) >= 6:
        artifactory_api_key = sys.argv[1]
        Rundeck_Auth_Token = sys.argv[2]
        inputs = sys.argv[3]
        git_token = sys.argv[4]
        git_user = sys.argv[5]
        run_id = sys.argv[6] 
        branch_name = 'feature/FE_'+ year + '_' + run_id + '_RD'
        
        #Export jobs for selected project
        Projects = inputs.split(",")
        Pro = Projects
        if len(Projects) >= 1:
            print ("Selected projects::",Projects)
            cleanup_workspace()
            with ZipFile(zip_filename, 'w') as f:
                for project_name in Pro:
                    filename = export_jobs(project_name)
                    f.write(filename)
                    filenames.append('rundeck/job_exports/'+filename) 
                    
            print("Filenames::",filenames) 
            #Clone repository --> create branch --> add changes --> commit --> push
            git_add(filenames,git_user,git_token,run_id) 
            #Create puull/merge request
            create_pull_request(git_token)            
            #Upload package in artifactory 
            artifactory_file_upload()
            print ("Zip file Name::",zip_filename)
            #Cleanup files
            cleanup_workspace()
        else:
            raise Exception("ERROR: No project selected for export")
    else:
        example = 'python  Export-Rundeck-Jobs.py <artifactory_token> <rundeck_token>'
        raise Exception(f'Wrong number of arguments. Example usage:\n{example}')
