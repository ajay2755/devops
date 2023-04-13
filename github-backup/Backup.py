import requests
import yaml
import json
import os
import datetime
import shutil

CONFIG_FILEPATH = "./config.yaml"

def start_backup():
    config = readConfig()
    repos = getAllRepos(config)
    folderPath = makeWeeklyFolder(config)
    backup_all_repos(repos, config, folderPath)
    compressWeeklyBackup(folderPath)
    return None

def readConfig():
    with open(CONFIG_FILEPATH, "r") as stream:
        data = yaml.safe_load(stream)
    return data

def makeWeeklyFolder(config):
    folderName = str(datetime.datetime.now().strftime("%d%m%Y"))
    BACKUP_DIR = config["Github"]["backup_repo_directory"]
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)
    path = f"{BACKUP_DIR}/{folderName}"
    os.mkdir(path)
    return path
    

def getAllRepos(config):
    repos = []
    GITHUB_ORG = config["Github"]["organisation_name"]
    GET_ALL_ORG_REPOS_API = config["Github"]["get_all_organisation_repos_api"].format(organisation=GITHUB_ORG)
    GITHUB_PAT = config["Github"]["github_personal_access_token"]
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_PAT}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.get(GET_ALL_ORG_REPOS_API, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.content.decode())
        for repo in data:
            repos.append(repo["full_name"])
    return repos

def backup_all_repos(repos, config, folderPath):
    GITHUB_BASE_URL_SSH = config["Github"]["github_ssh_base_url"]
    for repo in repos:
        repo_ssh = GITHUB_BASE_URL_SSH.format(full_name=repo)
        os.system(f"cd {folderPath} && git clone --mirror {repo_ssh}")
        
def compressWeeklyBackup(folderPath):
    temp = folderPath.split("/")
    folderName = temp[1]
    backupFolderRoot = temp[0]
    shutil.make_archive(folderName,"zip", folderPath)
    os.system(f"cd Github_Backup && rm -rf {folderName}")
    os.system(f"mv {folderName}.zip Github_Backup")
    return None
        
if __name__ == "__main__":
    start_backup()
    