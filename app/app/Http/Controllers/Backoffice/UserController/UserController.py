from app.Domain.User.Services.UserService import UserService
from app.Http.Requests.Backoffice.UserController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.UserController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.UserController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.UserController.UserCollectionResource import UserCollectionResource
from app.Http.Resources.Backoffice.UserController.UserResource import UserResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class UserController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "user.view": ["index", "show"],
            "user.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = UserService().search(params).paginate()
        return UserCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params = request.params
        user = UserService().create(params)

        return UserResource(user, status=status.HTTP_201_CREATED)

    def show(self, request, id):
        user = UserService().getById(id)
        return UserResource(user, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        user = UserService().update(id, params)

        return UserResource(user, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        UserService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
