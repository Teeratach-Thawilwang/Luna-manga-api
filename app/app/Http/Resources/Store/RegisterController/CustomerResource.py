from app.Services.LocalTime import localTime
from django.http import JsonResponse


class CustomerResource(JsonResponse):
    def __init__(self, customer, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": customer.id,
            "email": customer.email,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
