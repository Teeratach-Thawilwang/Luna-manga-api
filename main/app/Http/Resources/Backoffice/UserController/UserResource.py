from app.Domain.User.Models.User import User
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class UserResource(JsonResponse):
    def __init__(self, user: User, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": user.id,
            "email": user.email,
            "nick_name": user.nick_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "status": user.status,
            "created_at": localTime(user.created_at),
            "updated_at": localTime(user.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
