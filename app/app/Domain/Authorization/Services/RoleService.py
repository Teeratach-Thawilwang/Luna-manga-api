from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone

from app.Domain.Authorization.Models.ModelHasRole import ModelHasRole
from app.Domain.Authorization.Models.Permission import Permission
from app.Domain.Authorization.Models.Role import Role
from app.Domain.Customer.Models.Customer import Customer
from app.Domain.User.Models.User import User
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate


class RoleService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id", "name"]
        self.querySet = Role.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> Role:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Role:
        return self.querySet.create(**params)

    def update(self, id: int, params: dict[str, Any]) -> Role:
        params["updated_at"] = timezone.now()

        try:
            self.querySet.filter(pk=id).update(**params)
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteById(self, id: int) -> None:
        try:
            role = self.querySet.get(pk=id)
            role.delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def prefetch(self, *relations: Any):
        self.querySet = self.querySet.prefetch_related(*relations)
        return self

    def search(self, params: dict[str, Any]):
        if "q" in params:
            q: str = params["q"][0]
            if q.isnumeric():
                self.query += [Q(id__exact=q)]
            else:
                self.query += [Q(name__istartswith=q)]

        if "page" in params:
            self.page = int(params["page"][0])

        if "per_page" in params:
            self.perPage = int(params["per_page"][0])

        if "order_by" in params:
            self.orderBy = params["order_by"]

        return self

    def paginate(self) -> list:
        self.prefetch("modelhasrole_set__model", "has_permissions")
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)

    def addPermissions(self, role: Role, permisions: Permission) -> None:
        for permision in permisions:
            role.permission().add(permision)

    def removePermissions(self, role: Role, permisions: Permission) -> None:
        for permision in permisions:
            role.permission().remove(permision)

    def syncPermission(self, roleId: int, permissionIds: list[int]) -> None:
        deletePermisisonIds = []
        role = self.getById(roleId)
        currentPermissionIds = [permission["id"] for permission in role.permissions().values("id")]

        for permissionId in currentPermissionIds:
            if permissionId not in permissionIds:
                deletePermisisonIds.append(permissionId)

            if permissionId in permissionIds:
                index = permissionIds.index(permissionId)
                permissionIds.pop(index)

        addPermisions = Permission.objects.filter(id__in=permissionIds)
        deletePermisions = Permission.objects.filter(id__in=deletePermisisonIds)
        self.addPermissions(role, addPermisions)
        self.removePermissions(role, deletePermisions)

    def createModelHasRole(self, roleId: int, modelId: int, modelType: str) -> None:
        params = {
            "role_id": roleId,
            "model_id": modelId,
            "model_type": modelType,
        }
        ModelHasRole.objects.create(**params)

    def syncModelHasRole(self, roleId: int, modelIds: int, type: str = "user"):
        if type == "user":
            modelType = ContentType.objects.get_for_model(User)
        elif type == "customer":
            modelType = ContentType.objects.get_for_model(Customer)
        else:
            raise ResourceNotFoundException({"message": "model type invalid"})

        modelHasRoles = ModelHasRole.objects.filter(**{"role_id": roleId, "model_type": modelType})
        for modelHasRole in modelHasRoles:
            modelId = modelHasRole.model_id
            if modelId not in modelIds:
                modelHasRole.delete()

            if modelId in modelIds:
                index = modelIds.index(modelId)
                modelIds.pop(index)

        for modelId in modelIds:
            self.createModelHasRole(roleId, modelId, modelType)
