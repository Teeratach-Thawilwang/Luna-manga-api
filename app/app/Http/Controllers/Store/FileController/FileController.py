import json

from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import status, viewsets

from app.Domain.Customer.Models.Customer import Customer
from app.Domain.File.Services.FileService import FileService
from app.Enums.CollectionEnum import CollectionEnum
from app.Exceptions.CollectionInvalidException import CollectionInvalidException
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.FileController.ShowRequest import ShowRequest
from app.Http.Requests.Store.FileController.StoreRequest import StoreRequest
from app.Http.Resources.Backoffice.FileController.FileResource import FileResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Providers.CloudFrontService import CloudFrontService


class FileController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["store"]

        super().initial(request, *args, **kwargs)

    def store(self, request):
        StoreRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        params: dict = request.params
        uploadFile = params["file"][0]
        collection = CollectionEnum().get(params["collection_name"])

        if collection is None:
            raise CollectionInvalidException({"message": "Collection Not Found."})

        fileService = FileService()
        file = fileService.create(uploadFile, collection)

        isSync = json.loads(params.get("is_sync", "True").lower())
        fileService.uploadFileToStorage(file, uploadFile, collection, isSync)

        return FileResource(file, status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS))
    # @method_decorator(vary_on_headers("Authorization"))
    def show(self, request, uuid):
        ShowRequest(request)

        params = request.params
        conversion = None
        if "conversion" in params:
            conversion = params["conversion"][0]

        file = FileService().getByUuid(uuid)

        url = CloudFrontService().getCloudFrontSignedUrl(file, conversion)
        return redirect(url)
