from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet

from app.Domain.CustomerTracking.Models.CustomerTracking import CustomerTracking
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate


class CustomerTrackingService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id"]
        self.querySet = CustomerTracking.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id) -> CustomerTracking:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> CustomerTracking:
        return self.querySet.get_or_create(**params, defaults=params)

    def search(self, params):
        if "q" in params:
            q: str = params["q"][0]
            self.query += [Q(id__exact=q) | Q(model_id__exact=q)]

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
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)
