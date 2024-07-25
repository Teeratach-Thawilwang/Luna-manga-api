from typing import Any

from app.Domain.Bookmark.Models.Bookmark import Bookmark
from app.Enums.OrderByEnum import OrderByEnum
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate
from django.db.models import Q
from django.db.models.query import QuerySet


class BookmarkService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id"]
        self.querySet = Bookmark.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> Bookmark:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Bookmark:
        return self.querySet.get_or_create(**params, defaults=params)

    def deleteBy(self, params: dict[str, Any]) -> None:
        try:
            model = self.querySet.filter(**params)
            model.delete()
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
                self.query += [Q(name__istartswith=q)]

        if "start_date" in params:
            self.query += [Q(created_at__gte=params["start_date"][0])]

        if "end_date" in params:
            self.query += [Q(created_at__lte=params["end_date"][0])]

        if "page" in params:
            self.page = int(params["page"][0])

        if "per_page" in params:
            self.perPage = int(params["per_page"][0])

        if "order_by" in params:
            orderBy = params["order_by"]
            self.orderBy = orderBy

            if orderBy[0] == OrderByEnum.ASC:
                self.orderBy = ["id"]
            if orderBy[0] == OrderByEnum.DESC:
                self.orderBy = ["-id"]

        # For front-side
        if "customer_id" in params:
            self.query += [Q(customer_id=params["customer_id"])]

        if "story_status_in" in params:
            self.query += [Q(story__status__in=params["story_status_in"])]

        return self

    def paginate(self) -> list:
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)
