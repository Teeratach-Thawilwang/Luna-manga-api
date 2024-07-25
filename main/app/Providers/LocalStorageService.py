import os
import shutil

from app.Providers.StorageInterface import StorageInterface
from django.conf import settings


# Design for testing
# Bucket directory    : /storage/localFIles/
# Temporary directory : /storage/temporary/
class LocalStorageService(StorageInterface):
    def __init__(self) -> None:
        self.bucket = settings.STORAGE["BUCKET"]
        self.temporaryPath = settings.TEMPORARY_DIR

    def downloadToInMemory(self, sourcePath):
        # Download from bucket to in-memory
        sourcePath = self.bucket + "/" + sourcePath
        return open(sourcePath, "rb")

    def upload(self, sourcePath, destinationPath, contentType):
        # Upload from temporary to bucket
        destinationPath = self.bucket + "/" + destinationPath
        sourcePath = self.temporaryPath + sourcePath

        os.makedirs(os.path.dirname(destinationPath), exist_ok=True)
        shutil.copy(sourcePath, destinationPath)
        os.remove(sourcePath)

    def uploadInMemoryFile(self, uploadFile, destinationPath, contentType):
        # Upload from in-memory to bucket
        destinationPath = self.bucket + "/" + destinationPath

        os.makedirs(os.path.dirname(destinationPath), exist_ok=True)
        with open(destinationPath, "wb") as destinationFile:
            shutil.copyfileobj(uploadFile, destinationFile)

    def delete(self, sourcePath):
        sourcePath = self.bucket + "/" + sourcePath
        os.remove(sourcePath)
