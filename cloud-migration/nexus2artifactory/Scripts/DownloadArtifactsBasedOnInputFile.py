import os
import logging
import requests
import json
import yaml

# This script will download all the artifacts based on the given input files that contains the paths of the artifacts.
# The downloaded artifacts will be stored under the Artifacts folder.

CONFIG_FILEPATH = "./config.yaml"

def readConfig():
    with open(CONFIG_FILEPATH, "r") as stream:
        data = yaml.safe_load(stream)
    INPUT_FILEDIR = data["Directories"]["Input_Folder"]
    ARTIFACTS_DOWNLOAD_FOLERPATH = data["Directories"]["Artifact_Downloads_Folder"]
    API = data["Nexus"]["Download_Artifact_Assets_API"]
    return INPUT_FILEDIR, ARTIFACTS_DOWNLOAD_FOLERPATH, API
    

def readFile(repo, INPUT_FILEDIR):
    INPUT_FILEPATH = f"{INPUT_FILEDIR}/{repo}_output.txt"
    file = open(INPUT_FILEPATH, "r")
    return file

def downloadArtifact(repo, group, name, version, API, ARTIFACTS_DOWNLOAD_FOLERPATH):
    target = API.format(repo=repo, group=group, name=name, version=version).strip()
    logging.info(f"Target url: {target}")
    data = requests.get(target)
    logging.debug(f"Status Code: {data.status_code}")
    logging.debug(f"Content: \n{data.content}")
    if data.status_code != 200:
        print("Failed to locate target repo: ", data.status_code)
        exit(1)
    content = data.content
    jsonContent = json.loads(content)
    assets = jsonContent["items"]
    if len(assets) == 0:
       logging.warning(f"Asset component not found: {repo}/{group}/{name}/{version}")
    else:
        dir = setupFolder(repo, group, name, version, ARTIFACTS_DOWNLOAD_FOLERPATH)
        print(dir)
        for asset in assets:
            downloadUrl = asset["downloadUrl"]
            path = downloadUrl.split("repository")[1]
            directories = path.split("/")
            fileName = directories[-1]
            logging.debug(f"Filename: {fileName}")
            artifactDownload = requests.get(downloadUrl)
            artifactContent = artifactDownload.content
            artifactPath = f"{dir}/{fileName}"
            artifact = open(artifactPath, "wb")
            artifact.write(artifactContent)
            artifact.close()

def setupFolder(repo, group, name, version, ARTIFACTS_DOWNLOAD_FOLERPATH):
    currentDir = os.getcwd()
    gp = "/".join(group.split("."))
    path = currentDir + f"{ARTIFACTS_DOWNLOAD_FOLERPATH}/{repo}/{gp}/{name}/{version}"
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def downloadFromFile(repo=None):
    INPUT_FILEDIR, ARTIFACTS_DOWNLOAD_FOLERPATH, API = readConfig()
    if repo == None:
        repo = input("Nexus Repo to download:")
    file = readFile(repo, INPUT_FILEDIR)
    line = file.readline().strip()
    while line != "":
        valueSplit = line.split("/")
        repo = valueSplit[0].strip()
        group = valueSplit[1].strip()
        component = valueSplit[2].strip()
        version = valueSplit[3].strip()
        downloadArtifact(repo, group, component, version, API, ARTIFACTS_DOWNLOAD_FOLERPATH)
        line = file.readline().strip()
    return None

def downloadFromInput():
    INPUT_FILEDIR, ARTIFACTS_DOWNLOAD_FOLERPATH, API = readConfig()
    print("Please provide artifact location in this format <repository/group/component/version>")
    print("For example for atslib version 22.3.12.0 that is located under RELEASE/sg/sparksystems/ats in Nexus, please key in RELEASE/sg.sparksystems.ats/atslib/22.3.12.0")
    value = input("Input: ").strip()
    valueSplit = value.split("/")
    repo = valueSplit[0].strip()
    group = valueSplit[1].strip()
    component = valueSplit[2].strip()
    version = valueSplit[3].strip()
    downloadArtifact(repo, group, component, version, API, ARTIFACTS_DOWNLOAD_FOLERPATH)
    
