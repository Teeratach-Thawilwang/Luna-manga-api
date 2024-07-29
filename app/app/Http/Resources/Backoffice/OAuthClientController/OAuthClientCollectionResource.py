from app.Services.LocalTime import localTime
from django.http import JsonResponse


class OAuthClientCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for oAuthClient in self.data["data"]:
            data.append(
                {
                    "id": oAuthClient.id,
                    "name": oAuthClient.name,
                    "client_id": oAuthClient.client_id,
                    "client_secret": oAuthClient.client_secret,
                    "created_at": localTime(oAuthClient.created_at),
                    "updated_at": localTime(oAuthClient.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
