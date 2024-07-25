from app.Services.LocalTime import localTime
from django.http import JsonResponse


class BannerCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for banner in self.data["data"]:
            data.append(
                {
                    "id": banner.id,
                    "name": banner.name,
                    "type": banner.type,
                    "status": banner.status,
                    "created_at": localTime(banner.created_at),
                    "updated_at": localTime(banner.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
