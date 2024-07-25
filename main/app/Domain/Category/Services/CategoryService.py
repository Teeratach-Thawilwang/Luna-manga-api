from sys import modules
from typing import Any

from app.Domain.Category.Models.Category import Category
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Enums.OrderByEnum import OrderByEnum
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone

if "FileableService" not in modules:
    from app.Domain.File.Services.FileableService import FileableService


class CategoryService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id", "name"]
        self.querySet = Category.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> Category:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Category:
        imageId = None

        if "image_id" in params:
            imageId = params["image_id"]
            del params["image_id"]

        category = self.querySet.create(**params)
        if imageId != None:
            FileableService().syncSingleFileable(category.id, "category", imageId, CollectionNameEnum.CATEGORY_IMAGE)
        return category

    def update(self, id: int, params: dict[str, Any]) -> Category:
        imageId = None
        params["updated_at"] = timezone.now()

        if "image_id" in params:
            imageId = params["image_id"]
            del params["image_id"]

        try:
            self.querySet.filter(pk=id).update(**params)
            if imageId != None:
                FileableService().syncSingleFileable(id, "category", imageId, CollectionNameEnum.CATEGORY_IMAGE)
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteById(self, id: int) -> None:
        try:
            model = self.querySet.get(pk=id)
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
            orderBy = params["order_by"]
            self.orderBy = orderBy

            if orderBy[0] == OrderByEnum.ASC:
                self.orderBy = ["id"]
            if orderBy[0] == OrderByEnum.DESC:
                self.orderBy = ["-id"]

        return self

    def paginate(self) -> list:
        self.prefetch("fileable__file")
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)
