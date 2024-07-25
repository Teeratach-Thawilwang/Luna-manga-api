from app.Services.LocalTime import localTime
from django.http import JsonResponse


class RoleCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for role in self.data["data"]:
            data.append(
                {
                    "id": role.id,
                    "name": role.name,
                    "description": role.description,
                    "total_user": role.modelhasrole_set.count(),
                    "created_at": localTime(role.created_at),
                    "updated_at": localTime(role.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
