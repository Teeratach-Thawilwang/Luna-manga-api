from app.Domain.Authorization.Models.Permission import Permission
from app.Domain.Authorization.Models.Role import Role
from app.Domain.Authorization.Services.RoleService import RoleService
from app.Settings.permission import permission as permissionConfigs


class PermissionSeeder:
    def create(self):
        permissions = list(permissionConfigs.keys())
        for permission in permissions:
            if not Permission.objects.filter(name=permission).exists():
                params = {"name": permission, "guard_name": "backoffice"}
                Permission.objects.create(**params)
        Permission.objects.exclude(name__in=permissions).delete()

        role = Role.objects.filter(name="super-admin").first()
        if role is None:
            params = {
                "guard_name": "backoffice",
                "name": "super-admin",
                "description": "super-admin",
            }
            role = Role.objects.create(**params)
        permissionIds = list(Permission.objects.all().values_list("id", flat=True))
        RoleService().syncPermission(role.id, permissionIds)
