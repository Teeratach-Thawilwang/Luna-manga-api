from app.Services.LocalTime import localTime
from django.http import JsonResponse


class UserCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for user in self.data["data"]:
            data.append(
                {
                    "id": user.id,
                    "email": user.email,
                    "nick_name": user.nick_name,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "status": user.status,
                    "created_at": localTime(user.created_at),
                    "updated_at": localTime(user.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
