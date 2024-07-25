import json
from datetime import datetime, timedelta, timezone
from io import BytesIO

import requests
import rsa
from app.Domain.File.Models.File import File
from botocore.exceptions import ClientError
from botocore.signers import CloudFrontSigner
from django.conf import settings


class CloudFrontService:
    def __init__(self) -> None:
        self.client = self.createCloudFrontClient()
        self.policyCode = None

    @staticmethod
    def rsaSign(message):
        private_key = rsa.PrivateKey.load_pkcs1(settings.CLOUD_FRONT_RSA_SIGNER.encode("utf-8"))
        return rsa.sign(message, private_key, "SHA-1")

    def createCloudFrontClient(self):
        return CloudFrontSigner(settings.CLOUD_FRONT_KEY_ID, self.rsaSign)

    def downloadToInMemory(self, sourcePath):
        # Download from CloudFront to in-memory
        expireAt = datetime.now(timezone.utc) + timedelta(seconds=int(settings.CLOUD_FRONT_LINK_EXPIRED_IN_SECOND))
        try:
            signedUrl = self.client.generate_presigned_url(settings.CLOUD_FRONT_BASE_URL + sourcePath, date_less_than=expireAt)
            response = requests.get(signedUrl)
            response.raise_for_status()

            return BytesIO(response.content)
        except ClientError as e:
            print(e)

    def createPolicyCode(self):
        if self.client is None:
            self.client = self.createCloudFrontClient()

        url = f"{settings.CLOUD_FRONT_BASE_URL}*"
        expiredAt = datetime.now(timezone.utc) + timedelta(seconds=int(settings.CLOUD_FRONT_LINK_EXPIRED_IN_SECOND))
        policy = {
            "Statement": [
                {
                    "Resource": url,
                    "Condition": {
                        "DateLessThan": {
                            "AWS:EpochTime": int(expiredAt.timestamp()),
                        },
                    },
                },
            ]
        }
        policy_json = json.dumps(policy).encode("utf-8")
        presigned = self.client.generate_presigned_url(url, policy=policy_json)
        return presigned.replace(url, "")

    def generatePresignedUrl(self, url: str):
        if self.policyCode is None:
            self.policyCode = self.createPolicyCode()

        return f"{url}{self.policyCode}"

    def getFileConversion(self, file: File):
        if file.conversion is None:
            return []

        conversions = list(json.loads(file.conversion))
        if "original" in conversions:
            conversions.remove("original")
        return conversions

    def getCloudFrontSignedUrl(self, file: File, conversionName: str = None):
        if self.client is None:
            self.client = self.createCloudFrontClient()

        conversions = self.getFileConversion(file)
        extension = "." + file.file_name.split(".")[-1]
        if conversionName in conversions:
            fileUrl = f"{settings.CLOUD_FRONT_BASE_URL}{file.id}/{file.uuid}_{conversionName}{extension}"
        elif len(conversions) != 0:
            conversionName = conversions[-1]
            if conversionName != "thumbnail":
                fileUrl = f"{settings.CLOUD_FRONT_BASE_URL}{file.id}/{file.uuid}_{conversionName}{extension}"
            else:
                fileUrl = f"{settings.CLOUD_FRONT_BASE_URL}{file.id}/{file.uuid}{extension}"
        else:
            fileUrl = f"{settings.CLOUD_FRONT_BASE_URL}{file.id}/{file.uuid}{extension}"

        return self.generatePresignedUrl(fileUrl)
