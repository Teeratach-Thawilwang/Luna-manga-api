from app.Exceptions.PermissionException import PermissionException
from rest_framework.permissions import BasePermission


class UserPermissionMiddleware(BasePermission):
    def has_permission(self, request, view):
        owner = request.user
        requestMethod = str(request.method).lower()
        viewMethod = view.action_map[requestMethod]
        permissions = request.permissions

        for permission, method in permissions.items():
            if viewMethod in method:
                if owner is None:
                    raise PermissionException({"messages": "User has no permission."})
                if owner.hasPermission(permission):
                    return True
                raise PermissionException({"messages": "User has no permission."})

        return True
