from app.Domain.CustomerGroup.Models.CustomerGroup import CustomerGroup
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class CustomerGroupResource(JsonResponse):
    def __init__(self, customerGroup: CustomerGroup, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": customerGroup.id,
            "name": customerGroup.name,
            "status": customerGroup.status,
            "created_at": localTime(customerGroup.created_at),
            "updated_at": localTime(customerGroup.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
