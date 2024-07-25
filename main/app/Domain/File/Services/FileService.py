import io
import uuid
from typing import Any, BinaryIO

import magic
from app.Domain.File.Models.File import File
from app.Enums.ImageMimeTypeEnum import ImageMimeTypeEnum
from app.Exceptions.CollectionInvalidException import CollectionInvalidException
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Providers.StorageManager import StorageManager
from app.Services.ConversionService import ConversionService
from app.Services.Paginator import paginate
from django.db.models import Q
from django.db.models.query import QuerySet


class FileService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id"]
        self.querySet = File.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> File:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def getByUuid(self, uuid: str) -> File:
        try:
            return self.querySet.get(uuid=uuid)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, uploadFile: BinaryIO, collection: dict[str, Any]) -> File:
        mimeType = self.getMimeType(uploadFile)
        if mimeType not in collection["mimetypes"]:
            raise CollectionInvalidException({"message": "Collection not match with mimetype."})

        conversion = None
        if collection["conversion"] is not None:
            image = ConversionService().openFromUploadFile(uploadFile)
            conversion = ConversionService().transfromConversionByCollection(image, collection)
            conversion = str(conversion).replace("'", '"')

        params = {
            "file_name": uploadFile.name,
            "mime_type": mimeType,
            "collection_name": collection["name"],
            "conversion": conversion,
            "size_bytes": uploadFile.size,
            "uuid": uuid.uuid4().hex,
        }
        return self.querySet.create(**params)

    def deleteById(self, id: int) -> None:
        try:
            file = self.querySet.get(pk=id)
            file.delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def prefetch(self, *relations: tuple):
        self.querySet = self.querySet.prefetch_related(*relations)
        return self

    def search(self, params: dict[str, Any]):
        if "q" in params:
            q: str = params["q"][0]
            if q.isnumeric():
                self.query += [Q(id__exact=q)]
            else:
                self.query += [Q(file_name__startswith=q)]

        if "is_only_image" in params:
            if params["is_only_image"]:
                self.query += [Q(file_name__startswith=ImageMimeTypeEnum.list())]

        if "page" in params:
            self.page = int(params["page"][0])

        if "per_page" in params:
            self.perPage = int(params["per_page"][0])

        if "order_by" in params:
            self.orderBy = params["order_by"]

        return self

    def paginate(self) -> list:
        self.prefetch("modelhasrole_set__model", "has_permissions")
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)

    def getMimeType(self, uploadFile: BinaryIO):
        initialPosition = uploadFile.tell()
        uploadFile.seek(0)
        mimeType = magic.from_buffer(uploadFile.read(2048), mime=True)
        uploadFile.seek(initialPosition)
        return mimeType

    def createUploadFileFromFile(self, file: File):
        response = StorageManager(file).download(None)
        fileData = response.read()
        uploadFile = io.BytesIO(fileData)
        uploadFile.name = file.file_name
        uploadFile.size = len(fileData)
        uploadFile.seek(0)

        return uploadFile

    def getCollectionNamesFromFileIds(self, fileIds: int) -> list[str]:
        return File.objects.filter(id__in=fileIds).distinct().values_list("collection_name")
