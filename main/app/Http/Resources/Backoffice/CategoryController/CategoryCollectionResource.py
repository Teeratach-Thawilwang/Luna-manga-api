from app.Domain.Category.Services.CategoryService import CategoryService
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class CategoryCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for category in self.data["data"]:
            data.append(
                {
                    "id": category.id,
                    "name": category.name,
                    "total_story": category.story_set.count(),
                    "type": category.type,
                    "status": category.status,
                    "created_at": localTime(category.created_at),
                    "updated_at": localTime(category.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
