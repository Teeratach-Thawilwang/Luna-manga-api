from app.Domain.Category.Models.Category import Category
from app.Domain.File.Services.FileableService import FileableService
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class CategoryResource(JsonResponse):
    def __init__(self, category: Category, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": category.id,
            "name": category.name,
            "type": category.type,
            "status": category.status,
            "images": FileableService().transformImagesByCollection(category.fileable, CollectionNameEnum.CATEGORY_IMAGE),
            "created_at": localTime(category.created_at),
            "updated_at": localTime(category.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
