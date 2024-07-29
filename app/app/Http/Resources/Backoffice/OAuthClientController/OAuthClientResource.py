from app.Services.LocalTime import localTime
from django.http import JsonResponse


class OAuthClientResource(JsonResponse):
    def __init__(self, oAuthClient, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": oAuthClient.id,
            "name": oAuthClient.name,
            "client_id": oAuthClient.client_id,
            "client_secret": oAuthClient.client_secret,
            "created_at": localTime(oAuthClient.created_at),
            "updated_at": localTime(oAuthClient.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
