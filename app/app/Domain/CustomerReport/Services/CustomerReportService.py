from typing import Any

from app.Domain.CustomerReport.Models.CustomerReport import CustomerReport
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Helpers import transformStringToBoolean
from app.Services.Paginator import paginate
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone


class CustomerReportService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id"]
        self.querySet = CustomerReport.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id) -> CustomerReport:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> CustomerReport:
        if "source" in params:
            params["model_type"] = ContentType.objects.get(model=params["source"])
            del params["source"]

        return self.querySet.get_or_create(**params, defaults=params)

    def update(self, id: int, params: dict[str, Any]) -> CustomerReport:
        params["updated_at"] = timezone.now()

        if "is_accept" in params:
            isAccept = params["is_accept"]
            if not isAccept:
                params["accept_by"] = None

        try:
            self.querySet.filter(pk=id).update(**params)
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def search(self, params):
        if "q" in params:
            q: str = params["q"][0]
            self.query += [Q(id__exact=q) | Q(model_id__exact=q)]

        if "group" in params:
            self.query += [Q(group__exact=params["group"][0])]

        if "source" in params:
            modelType = ContentType.objects.get(model=params["source"][0])
            self.query += [Q(model_type__exact=modelType)]

        if "is_accept" in params:
            isAccept = transformStringToBoolean(params["is_accept"][0])
            self.query += [Q(is_accept=isAccept)]

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
