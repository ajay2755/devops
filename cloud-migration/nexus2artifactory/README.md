# Description
This folder contains all the files used for the migration of on-prem Nexus to Artifactory

# Scripts
There are a total of 4 scripts for this migration, but the entry point will be the `Nexus2ArtifactoryMigration.py` script. This is the only script that the user will need to execute.

**Nexus2ArtifactoryMigration.py** - This is the script that the user will run. It contains 3 stages (Download artifact paths, Download artifacts locally and Push to Artifactory). This script also provides the option for users to run any of the other 3 scripts individually or to execute the entire migration process.

**NexusRepositoryNameDownload.py** - This script will query for all the artifacts that are located under the specified Nexus repo and write the artifact path to a text file to allow for bulk downloading later on. 

**DownloadArtifactsBasedOnInputFile.py** - This script will read the list of artifacts to be downloaded from a text file located under RepositoryNameFolder. It also has the option to allow the user to manaually specify 1 artifact component to be downloaded.

**PushToArtifactory.py** - This script will push the entire local repo that is specified under the `Artifacts` folder.
