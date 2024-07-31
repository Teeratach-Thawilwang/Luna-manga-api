import json

from app.Domain.File.Models.File import File
from app.Enums.ImageMimeTypeEnum import ImageMimeTypeEnum
from app.Exceptions.CollectionInvalidException import CollectionInvalidException
from app.Providers.AwsStorageService import AwsStorageService
from app.Providers.LocalStorageService import LocalStorageService
from app.Services.ConversionService import ConversionService
from django.conf import settings


class StorageManager:
    __name__ = "StorageManager"

    def __init__(self, file: File):
        self.file = file
        self.client = None
        self.folderPath = f"{file.id}/"

    def __del__(self):
        del self.client

    def createClient(self):
        storageType = settings.STORAGE_TYPE
        match storageType:
            case "local":
                return LocalStorageService()
            case "s3":
                return AwsStorageService()

    def download(self, conversion):
        if self.client is None:
            self.client = self.createClient()

        if self.file.conversion is None or conversion is None:
            extension = self.file.file_name.split(".")[-1]
            sourcePath = f"{self.folderPath}{self.file.uuid}.{extension}"
            return self.client.downloadToInMemory(sourcePath)

        conversions = json.loads(self.file.conversion)
        if conversion not in list(conversions.keys()):
            raise CollectionInvalidException({"message": "Conversion Not Found."})

        extension = self.file.file_name.split(".")[-1]
        sourcePath = f"{self.folderPath}{self.file.uuid}_{conversion}.{extension}"
        return self.client.downloadToInMemory(sourcePath)

    def upload(self, uploadFile, collection):
        if self.client is None:
            self.client = self.createClient()

        imageMimeType = ImageMimeTypeEnum.list()

        if self.file.mime_type in imageMimeType:
            files = ConversionService().convertImageFromUploadFile(uploadFile, collection)
            for fileName in files:
                desPath = self.folderPath + fileName
                self.client.upload(fileName, desPath, self.file.mime_type)
        else:
            desPath = self.folderPath + uploadFile.name
            self.client.uploadInMemoryFile(uploadFile, desPath, self.file.mime_type)

    def delete(self):
        if self.client is None:
            self.client = self.createClient()

        if self.file.conversion is None:
            sourcePath = self.folderPath + self.file.file_name
            self.client.delete(sourcePath)
            return

        conversions = json.loads(self.file.conversion.replace("'", '"'))

        for key, value in conversions.items():
            extension = "." + self.file.file_name.split(".")[-1]
            fileName = self.file.file_name.replace(extension, "")
            sourcePath = self.folderPath + f"{fileName}_{key}{extension}"
            self.client.delete(sourcePath)

        sourcePath = f"{self.file.id}/{self.file.file_name}"
        self.client.delete(sourcePath)
