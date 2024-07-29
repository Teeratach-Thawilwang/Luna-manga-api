import copy
import os

import boto3
from app.Providers.StorageInterface import StorageInterface
from botocore.exceptions import ClientError
from django.conf import settings


# Bucket directory    : arn::s3/{BUCKET}/
# Temporary directory : /storage/temporary/
class AwsStorageService(StorageInterface):
    def __init__(self) -> None:
        self.client = self.createAwsS3Client()
        self.bucket = settings.STORAGE["BUCKET"]
        self.temporaryPath = settings.TEMPORARY_DIR

    def createAwsS3Client(self):
        params = {
            "aws_access_key_id": settings.STORAGE["ACCESS_KEY"],
            "aws_secret_access_key": settings.STORAGE["ACCESS_SECRET"],
            "region_name": settings.STORAGE["REGION"],
        }
        return boto3.client("s3", **params)

    def downloadToInMemory(self, sourcePath):
        # Download from bucket to in-memory
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=sourcePath)
            return response["Body"]
        except ClientError as e:
            print(e)

    def upload(self, sourcePath, destinationPath, contentType):
        # Upload from temporary to bucket
        sourcePath = self.temporaryPath + sourcePath
        try:
            extraArgs = {
                "ContentType": contentType,
            }
            self.client.upload_file(sourcePath, self.bucket, destinationPath, ExtraArgs=extraArgs)
        except ClientError as e:
            print(e)
        os.remove(sourcePath)

    def uploadInMemoryFile(self, uploadFile, destinationPath, contentType):
        # Upload from in-memory to bucket
        file = copy.deepcopy(uploadFile)
        try:
            extraArgs = {
                "ContentType": contentType,
            }
            self.client.upload_fileobj(file, self.bucket, destinationPath, ExtraArgs=extraArgs)
        except ClientError as e:
            print("uploadInMemoryFile", e)

    def delete(self, sourcePath):
        try:
            self.client.delete_object(Bucket=self.bucket, Key=sourcePath)
        except ClientError as e:
            print(e)
