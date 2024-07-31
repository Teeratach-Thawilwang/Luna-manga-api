from app.Domain.Authorization.Models.ModelHasRole import ModelHasRole
from app.Domain.Authorization.Models.Permission import Permission
from app.Domain.Authorization.Models.Role import Role
from app.Domain.User.Models.User import User
from app.Http.Resources.Backoffice.PermissionController.PermissionCollectionResource import PermissionCollectionResource
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class UserProfileResource(JsonResponse):
    def __init__(self, user: User, status=200, safe=False, json_dumps_params=None, **kwargs):
        permissions = self.getUserPermissions(user)
        self.data = {
            "id": user.id,
            "email": user.email,
            "nick_name": user.nick_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "status": user.status,
            "permissions": PermissionCollectionResource({"data": permissions}).data["data"],
            "created_at": localTime(user.created_at),
            "updated_at": localTime(user.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def getUserPermissions(self, user: User) -> list[Permission]:
        userPermissions = set()
        modelHasRoles: list[ModelHasRole] = user.model_has_role.all()
        for modelHasRole in modelHasRoles:
            role: Role = modelHasRole.role
            permissions = role.has_permissions.all()

            for permission in permissions:
                if permission not in userPermissions:
                    userPermissions.add(permission)

        return list(userPermissions)
