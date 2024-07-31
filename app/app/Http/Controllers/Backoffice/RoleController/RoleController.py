from app.Domain.Authorization.Services.RoleService import RoleService
from app.Http.Requests.Backoffice.RoleController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.RoleController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.RoleController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.RoleController.RoleCollectionResource import RoleCollectionResource
from app.Http.Resources.Backoffice.RoleController.RoleResource import RoleResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class RoleController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "roles_and_permission.view": ["index", "show"],
            "roles_and_permission.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = RoleService().search(params).paginate()
        return RoleCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params = request.params
        roleParams = {
            "name": params["name"],
            "guard_name": getattr(params, "guard_name", "backoffice"),
            "description": params["description"],
        }
        roleService = RoleService().prefetch("modelhasrole_set__model", "has_permissions")
        role = roleService.create(roleParams)

        if "user_ids" in params:
            userIds = params["user_ids"]
            RoleService().syncModelHasRole(role.id, userIds, "user")

        if "permission_ids" in params:
            permissionIds = params["permission_ids"]
            RoleService().syncPermission(role.id, permissionIds)

        return RoleResource(role, status=status.HTTP_201_CREATED)

    def show(self, request, id):
        roleService = RoleService().prefetch("modelhasrole_set__model", "has_permissions")
        role = roleService.getById(id)
        return RoleResource(role, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        roleParams = {}
        if "name" in params:
            roleParams["name"] = params["name"]

        if "guard_name" in params:
            roleParams["guard_name"] = params["guard_name"]

        if "description" in params:
            roleParams["description"] = params["description"]

        roleService = RoleService().prefetch("modelhasrole_set__model", "has_permissions")
        role = roleService.update(id, roleParams)

        if "user_ids" in params:
            userIds = params["user_ids"]
            RoleService().syncModelHasRole(id, userIds, "user")

        if "permission_ids" in params:
            permissionIds = params["permission_ids"]
            RoleService().syncPermission(id, permissionIds)

        return RoleResource(role, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        RoleService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
