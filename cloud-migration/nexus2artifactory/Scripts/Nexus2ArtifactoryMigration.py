import NexusRepositoryNameDownload
import DownloadArtifactsBasedOnInputFile
import PushToArtifactory

if __name__ == "__main__":
    repo = input("Nexus Repo:")
    stage = input("Please choose what stage of migration you want to execute:\n1: Download artifacts names under specifc repository from Nexus\n2: Download all artifacts based on input file\n3: Push all artifacts to Artifactory\n4: Everything\n5: Exit\nPlease enter the stage number:")
    if stage == "1":
        NexusRepositoryNameDownload.start(repo)
    elif stage == "2":
        fromFile = input("Read from file or input? Type File / Input:")
        if fromFile == "File":
            DownloadArtifactsBasedOnInputFile.downloadFromFile(repo)
        elif fromFile == "Input":
            DownloadArtifactsBasedOnInputFile.downloadFromInput()
        else:
            raise Exception("Invalid input")
    elif stage == "3":
        PushToArtifactory.push(repo)
    elif stage == "4":
        NexusRepositoryNameDownload.start(repo)
        DownloadArtifactsBasedOnInputFile.downloadFromFile(repo)
        PushToArtifactory.push(repo)
    elif stage == "5":
        exit()
    else:
        raise Exception("Invalid stage number")