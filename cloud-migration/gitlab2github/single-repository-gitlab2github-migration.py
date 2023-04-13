import requests
import os
import json
import logging
import datetime
import yaml

CONFIG_FILEPATH = "./config.yaml"
LOGS_DIR = "./logs"
CURRENT_DIR = os.getcwd()

def setupLogs():
    log_file = str(datetime.datetime.now().strftime("%d%m%Y.%H%M%S")) + ".txt"
    if not os.path.exists(LOGS_DIR):
        os.mkdir(LOGS_DIR)
    LOG_FILE_PATH = f"{LOGS_DIR}/logs_{log_file}"
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", datefmt="%m-%d %H:%M", filename=LOG_FILE_PATH, filemode="w")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
    consoleLogger = logging.getLogger("root")
    consoleLogger.debug(f"Log file path: {LOG_FILE_PATH}")
    consoleLogger.info("Console Logger setup done")
    consoleLogger.info(f"Log file created at: {LOG_FILE_PATH}")
    
    return consoleLogger


def readConfig(logger):
    logger.info(f"Reading config file from: {CONFIG_FILEPATH}\n")
    with open(CONFIG_FILEPATH, "r") as stream:
        data = yaml.safe_load(stream)
    github_authentication_token = data["github_authentication_token"]
    github_organisation_name = data["github_organisation_name"]
    projects_to_migrate_filepath = data["projects_to_migrate_filepath"]
    github_create_org_repo_api = data["github_create_org_repo_api"]
    logger.debug(f"Github Auth Token: {github_authentication_token}")
    logger.debug(f"Github organisation: {github_organisation_name}")
    logger.debug(f"Project to migrate file location: {projects_to_migrate_filepath}\n")
    logger.debug(f"Github Organisation Create Repo API: {github_create_org_repo_api}")
    return github_authentication_token, github_organisation_name, projects_to_migrate_filepath, github_create_org_repo_api

def start(logger, projects_to_migrate_filepath, github_authentication_token, github_create_org_repo_api):
    logger.info(f"Reading project file from: {projects_to_migrate_filepath}")
    projectsFile = open(projects_to_migrate_filepath, "r")
    line = projectsFile.readline().strip()
    while (line != ""):
        data = line.split("/")
        repoOwner = data[0].strip()
        repoName = data[1].strip()
        try:
            pullFromGitlab(logger, repoOwner, repoName)
            createGithubRepo(logger, github_authentication_token, repoName, github_organisation_name, github_create_org_repo_api)
            pushToGithub(logger, github_organisation_name, repoName)
            logger.info(f"{line}: Success\n")
        except Exception as e:
            logger.error(f"{line}: Failed\n")
            logger.error(e)
        line = projectsFile.readline().strip()
    return None

def pullFromGitlab(logger, repoOwner, repoName):
    logger.info(f"Pulling from gitlab: {repoOwner}/{repoName}")
    os.system(f"git clone --mirror git@gitlab.sparksystems.sg:{repoOwner}/{repoName}.git")
 

def createGithubRepo(logger, token, repoName, github_organisation_name, github_create_org_repo_api):
    logger.info(f"Creating repository in Github: {github_organisation_name}/{repoName}")
    GITHUB_AUTH_TOKEN = token
    GITHUB_CREATE_ORG_REPO_URL = github_create_org_repo_api.format(github_organisation_name = github_organisation_name)
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_AUTH_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    logger.debug(f"Headers:\n{headers}")
    
    payload = {
        "name": repoName,
        "homepage":"https://github.com",
        "private": "true",
        "has_issues": "true"
    }
    
    logger.debug(f"Payload:\n{payload}")
    
    response = requests.post(GITHUB_CREATE_ORG_REPO_URL, headers=headers, data=json.dumps(payload))
    logger.debug(f"Response:\n{response}")
    return None

def pushToGithub(logger, github_organisation_name, repoName):
    logger.debug("Pushing to Github")
    GITHUB_ORG_REPO_SSH = f"git@github.com:{github_organisation_name}/{repoName}.git"
    logger.debug(GITHUB_ORG_REPO_SSH)
    os.system(f"cd {repoName}.git && pwd && git push --mirror {GITHUB_ORG_REPO_SSH}")
    return None


if __name__ == "__main__":
    logger = setupLogs()
    try: 
        github_authentication_token, github_organisation_name, projects_to_migrate_filepath, github_create_org_repo_api = readConfig(logger)
        start(logger, projects_to_migrate_filepath, github_authentication_token, github_create_org_repo_api)
    except Exception as e:
        logger.error(e)