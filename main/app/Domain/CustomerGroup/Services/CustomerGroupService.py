from typing import Any

from app.Domain.Customer.Models.Customer import Customer
from app.Domain.CustomerGroup.Models.CustomerGroup import CustomerGroup
from app.Exceptions.PermissionException import PermissionException
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone


class CustomerGroupService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id", "name"]
        self.querySet = CustomerGroup.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> CustomerGroup:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> CustomerGroup:
        return self.querySet.create(**params)

    def update(self, id: int, params: dict[str, Any]) -> CustomerGroup:
        if id == 1:
            raise PermissionException({"message": "Default customer group cannot be updated."})

        params["updated_at"] = timezone.now()

        try:
            self.querySet.filter(pk=id).update(**params)
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteById(self, id: int) -> None:
        if id == 1:
            raise PermissionException({"message": "Default customer group cannot be deleted."})

        try:
            customerGroup = self.querySet.get(pk=id)
            Customer.objects.filter(customer_group_id=id).update(customer_group_id=1)
            customerGroup.delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def prefetch(self, *relations: tuple):
        self.querySet = self.querySet.prefetch_related(*relations)
        return self

    def search(self, params: dict[str, Any]):
        if "q" in params:
            q: str = params["q"][0]
            if q.isnumeric():
                self.query += [Q(id__exact=q)]
            else:
                self.query += [Q(name__startswith=q)]

        if "status" in params:
            self.query += [Q(status__exact=params["status"][0])]

        if "start_date" in params:
            self.query += [Q(created_at__gte=params["start_date"][0])]

        if "end_date" in params:
            self.query += [Q(created_at__lte=params["end_date"][0])]

        if "page" in params:
            self.page = int(params["page"][0])

        if "per_page" in params:
            self.perPage = int(params["per_page"][0])

        if "order_by" in params:
            self.orderBy = params["order_by"]

        return self

    def paginate(self) -> list:
        self.prefetch("customer_set")
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)
