import requests
import json
import logging
import yaml

# This script will query for all the artifacts under the specified nexus repo and write the 
# artifact paths into a text file located under RepositoryNameFolder.
# The format of the artifact path will be written as <repo>/<group>/<component>/<version>

CONFIG_FILEPATH = "./config.yaml"

def readConfig():
    with open(CONFIG_FILEPATH, "r") as stream:
        data = yaml.safe_load(stream)
    return data

def setupLogging():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.info("Logging started")
    return logger

def createOutputFile(repo, logger, data):
    OUTPUT_FOLDER = data["Directories"]["Input_Folder"].strip()
    filename = f"{repo}_output.txt"
    path = f"../{OUTPUT_FOLDER}/{filename}"
    file = open(path, "a")
    logger.info(f"{filename} created")
    return file

def downloadPage(repo, continuationToken, pageNumber, file, logger, data):
    logger.info(f"Page {pageNumber}")
    if continuationToken == "":
        url = data["Nexus"]["Download_Artifact_Path_API"].format(repo=repo).strip()
    else:
        url = data["Nexus"]["Download_Artifact_Path_Continue_API"].format(repo=repo, continuationToken=continuationToken).strip()
        
    logger.info(f"Target Repo Url: {url}")
    data = requests.get(url)
    content = json.loads(data.content)
    logger.debug(content)
    continuationToken = content["continuationToken"]
    items = content["items"]
    logger.debug(items[0])
    for item in items:
        repo = item["repository"]
        group = item["group"]
        component = item["name"]
        version = item["version"]
        path = f"{repo}/{group}/{component}/{version}"
        logger.debug(f"Component target path: {path}")
        file.write(path + "\n")
    return continuationToken
   

def getComponentsFromRepo(repo, file, logger, data):
    continuationToken = ""
    pageNumber = 1
    while continuationToken != None:
        continuationToken = downloadPage(repo, continuationToken, pageNumber, file, logger, data)
        pageNumber += 1
    
    logger.info(f"{repo} artifact names retrieved ...")

def start(nexusRepo=None):
    data = readConfig()
    logger = setupLogging()
    if nexusRepo == None:
        nexusRepo = input("Repository to inspect:").strip()
    logger.info(f"Repository: {nexusRepo}")
    file = createOutputFile(nexusRepo, logger, data)
    getComponentsFromRepo(nexusRepo, file, logger)
    file.close()
    logger.info("Done ...")