import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import status, viewsets

from app.Domain.File.Services.FileService import FileService
from app.Enums.CollectionEnum import CollectionEnum
from app.Enums.EventEnum import EventEnum
from app.Event.Event import Event
from app.Exceptions.CollectionInvalidException import CollectionInvalidException
from app.Http.Requests.Backoffice.FileController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.FileController.ShowRequest import ShowRequest
from app.Http.Requests.Backoffice.FileController.StoreRequest import StoreRequest
from app.Http.Resources.Backoffice.FileController.FileCollectionResource import FileCollectionResource
from app.Http.Resources.Backoffice.FileController.FileResource import FileResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from app.Providers.CloudFrontService import CloudFrontService


class FileController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "store", "destroy"]
        request.permissions = {
            "file.view": ["index"],
            "file.manage": ["store", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = FileService().search(params).paginate()
        return FileCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params: dict = request.params
        uploadFile = params["file"][0]
        collection = CollectionEnum().get(params["collection_name"])

        if collection is None:
            raise CollectionInvalidException({"message": "Collection Not Found."})

        file = FileService().create(uploadFile, collection)
        extension = "." + uploadFile.name.split(".")[-1]
        uploadFile.name = file.uuid + extension

        isUpload = json.loads(params.get("is_upload", "True").lower())
        isSync = json.loads(params.get("is_sync", "True").lower())
        if isUpload:
            uploadParams = {
                "file": file,
                "uploadFile": uploadFile,
                "collection": collection,
                "isSync": isSync,
            }
            Event(EventEnum.UPLOAD_FILE, uploadParams)

        return FileResource(file, status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS))
    @method_decorator(vary_on_headers("Authorization"))
    def show(self, request, uuid):
        ShowRequest(request)

        params = request.params
        conversion = None
        if "conversion" in params:
            conversion = params["conversion"][0]

        file = FileService().getByUuid(uuid)

        url = CloudFrontService().getCloudFrontSignedUrl(file, conversion)
        return redirect(url)

    def test(self, request):
        url = "http://127.0.0.1/backoffice/file/2da245f394874fb6892785599fe27b00"
        video_url = "http://127.0.0.1/backoffice/file/961195a17c434cb6ad4b51e1ca4bac1c"
        return HttpResponse(f'<img src="{url}"><br><video width="320" height="240" controls><source src="{video_url}" type="video/mp4">Your browser does not support the video tag.</video>')

    def destroy(self, request, uuid):
        file = FileService().getByUuid(uuid)
        extension = "." + file.file_name.split(".")[-1]
        file.file_name = file.uuid + extension

        params = {
            "file": file,
        }
        Event(EventEnum.DELETE_FILE, params)

        file.delete()
        return HttpResponse(status=status.HTTP_200_OK)
