from app.Services.LocalTime import localTime
from django.http import JsonResponse


class TokenResource(JsonResponse):
    def __init__(self, oAuthToken, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "access_token": oAuthToken.access_token,
            "refresh_token": oAuthToken.refresh_token,
            "access_token_expired_day": 1,
            "refresh_token_expired_day": 7,
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
