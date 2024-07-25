from app.Domain.Authentication.Services.OAuthClientService import OAuthClientService
from app.Http.Requests.Backoffice.OAuthClientController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.OAuthClientController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.OAuthClientController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.OAuthClientController.OAuthClientCollectionResource import OAuthClientCollectionResource
from app.Http.Resources.Backoffice.OAuthClientController.OAuthClientResource import OAuthClientResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class OAuthClientController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "oauth_client.view": ["index", "show"],
            "oauth_client.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = OAuthClientService().search(params).paginate()
        return OAuthClientCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params = request.params
        oAuthClient = OAuthClientService().create(params)

        return OAuthClientResource(oAuthClient, status=status.HTTP_201_CREATED)

    def show(self, request, id):
        oAuthClient = OAuthClientService().getById(id)
        return OAuthClientResource(oAuthClient, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        oAuthClient = OAuthClientService().update(id, params)

        return OAuthClientResource(oAuthClient, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        OAuthClientService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
