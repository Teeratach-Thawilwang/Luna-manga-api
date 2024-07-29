from app.Domain.Authorization.Models.Permission import Permission
from app.Http.Resources.Backoffice.PermissionController.PermissionCollectionResource import PermissionCollectionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from rest_framework import viewsets


class PermissionController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index"]
        request.permissions = {
            "roles_and_permission.view": ["index"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        permissions = Permission.objects.all()
        return PermissionCollectionResource({"data": permissions})
