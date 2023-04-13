import os
import yaml
import logging

# This script will push the entire repository that is found locally onto Artifactory. The file directory hierarchy will also be maintained.

def check_artifactory_status():
    status = os.popen("jf rt ping").read()
    if status == "OK":
        return True
    else:
        return False

def push(repo=None):
    if repo == None:
        repo = input("Artifactory Target Repo:")
    with open("config.yaml", "r") as stream:
        data = yaml.safe_load(stream)
    status = check_artifactory_status()
    targetArtifactoryRepo = data["Artifactory"]["Target_Repo"]
    serverId = data["Artifactory"]["Server_Id"]
    logging.debug(f"TargetArtifactoryRepo: {targetArtifactoryRepo}")
    logging.debug(f"Artifactory ServerId: {serverId}")
    if status:
        logging.info("Pushing .jar and .pom files to Artifactory")
        os.system(f'cd {repo} & jf rt upload "./*/*.jar" {targetArtifactoryRepo} --server-id={serverId} --recursive=true & jf rt upload "./*/*.pom" {targetArtifactoryRepo} --server-id={serverId} --recursive=true')
    logging.info("Push complete")
    return None

