from django.http import JsonResponse

from app.Domain.File.Services.FileableService import FileableService
from app.Enums.CollectionEnum import CollectionNameEnum


class CategoryCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        fileableService = FileableService()
        for category in self.data["data"]:
            data.append(
                {
                    "id": category.id,
                    "name": category.name,
                    "type": category.type,
                    "images": fileableService.transformImagesByCollection(category.fileable.all(), CollectionNameEnum.CATEGORY_IMAGE, "store"),
                }
            )
        self.data["data"] = data
        return self.data
