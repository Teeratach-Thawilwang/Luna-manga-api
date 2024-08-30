from sys import modules
from typing import Any

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

from app.Domain.File.Models.File import File
from app.Domain.File.Models.Fileable import Fileable
from app.Enums.CachePagePrefixEnum import CachePagePrefixEnum
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Providers.CloudFrontService import CloudFrontService
from app.Services.Helpers import getCache, setCache

if "FileService" not in modules:
    from app.Domain.File.Services.FileService import FileService


class FileableService:
    def __init__(self):
        self.querySet = Fileable.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> Fileable:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def deleteById(self, id: int) -> None:
        try:
            fileable = self.querySet.get(pk=id)
            fileable.delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def prefetch(self, *relations: tuple):
        self.querySet = self.querySet.prefetch_related(*relations)
        return self

    def syncSingleFileable(self, modelId: int, modelType: str, fileId: int, collectionName: CollectionNameEnum) -> None:
        modelType = ContentType.objects.get(model=modelType)
        try:
            params = {
                "model_id": modelId,
                "model_type": modelType,
                "file_id": fileId,
            }
            if not self.querySet.filter(**params).exists():
                self.querySet.create(**params)

            params = {
                "model_id": modelId,
                "model_type": modelType,
                "file__collection_name": collectionName,
            }
            self.querySet.filter(**params).exclude(file_id=fileId).delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def syncFileableByFileIds(self, modelId: int, modelType: str, fileIds: list[int]) -> None:
        modelType = ContentType.objects.get(model=modelType)
        try:
            params = {
                "model_id": modelId,
                "model_type": modelType,
            }
            for fileId in fileIds:
                params["file_id"] = fileId
                if not self.querySet.filter(**params).exists():
                    self.querySet.create(**params)

            params = {
                "model_id": modelId,
                "model_type": modelType,
                "file__collection_name__in": FileService().getCollectionNamesFromFileIds(fileIds),
            }
            self.querySet.filter(**params).exclude(file_id__in=fileIds).delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def transformImagesByCollection(self, fileableSet: QuerySet, collectionName: CollectionNameEnum, sideUrl: str = "backoffice", useCloudFront: bool = True) -> list:
        transfromData = []
        fileables = fileableSet.filter(file__collection_name=collectionName)
        for fileable in fileables:
            file: File = fileable.file
            if useCloudFront:
                transfromData += [self.transformImagesUsingCloudFrontUrl(file)]
                continue
            transfromData += [self.transformImagesUsingAppUrl(file, sideUrl)]
        return transfromData

    def transformImagesUsingAppUrl(self, file: File, sideUrl: str = "backoffice"):
        fileUrl = f"{settings.APP_URL}/{sideUrl}/file/{file.uuid}"
        return {
            "id": file.id,
            "original": fileUrl,
            "desktop": f"{fileUrl}?conversion=desktop",
            "mobile": f"{fileUrl}?conversion=mobile",
            "thumbnail": f"{fileUrl}?conversion=thumbnail",
            "collection_name": file.collection_name,
        }

    def transformImagesUsingCloudFrontUrl(self, file: File):
        key = f"{CachePagePrefixEnum.PRESIGNED_URL}_{file.uuid}"
        data = getCache(key)
        if data != None:
            return data

        cloudFrontService = getCache("cloudfront_service")
        if cloudFrontService == None:
            cloudFrontService = CloudFrontService()
            seconds = int(settings.CLOUD_FRONT_LINK_EXPIRED_IN_SECOND)
            setCache("cloudfront_service", cloudFrontService, seconds)

        originalPresignedUrl = cloudFrontService.getCloudFrontSignedUrl(file)
        desktopPresignedUrl = cloudFrontService.getCloudFrontSignedUrl(file, "desktop")
        mobilePresignedUrl = cloudFrontService.getCloudFrontSignedUrl(file, "mobile")
        thumbnailPresignedUrl = cloudFrontService.getCloudFrontSignedUrl(file, "thumbnail")

        data = {
            "id": file.id,
            "original": originalPresignedUrl,
            "desktop": desktopPresignedUrl,
            "mobile": mobilePresignedUrl,
            "thumbnail": thumbnailPresignedUrl,
            "collection_name": file.collection_name,
        }
        seconds = int(settings.CACHE_PRESIGNED_URL_IN_SECONDS)
        setCache(key, data, seconds)

        return data

    def transformAudioByCollection(self, fileableSet: QuerySet, collectionName: CollectionNameEnum, sideUrl: str = "backoffice"):
        transfromData = []
        fileables = fileableSet.filter(file__collection_name=collectionName)
        for fileable in fileables:
            file: File = fileable.file
            fileUrl = f"{settings.APP_URL}/{sideUrl}/file/{file.uuid}"
            transfromData += [
                {
                    "id": file.id,
                    "url": fileUrl,
                    "collection_name": file.collection_name,
                }
            ]
        return transfromData
