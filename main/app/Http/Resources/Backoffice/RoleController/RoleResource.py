from app.Domain.Authorization.Models.Role import Role
from app.Http.Resources.Backoffice.UserController.UserCollectionResource import UserCollectionResource
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class RoleResource(JsonResponse):
    def __init__(self, role: Role, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "permissions": self.getPermissionInRole(role),
            "users": self.getUsersInRole(role),
            "created_at": localTime(role.created_at),
            "updated_at": localTime(role.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def getUsersInRole(self, role):
        users = []
        for model in role.modelHasRoles():
            users.append(model.model)
        return UserCollectionResource({"data": users}).data["data"]

    def getPermissionInRole(self, role):
        data = []
        for permission in role.permissions():
            data.append(
                {
                    "id": permission.id,
                    "name": permission.name,
                    "created_at": localTime(permission.created_at),
                    "updated_at": localTime(permission.updated_at),
                }
            )

        return data
