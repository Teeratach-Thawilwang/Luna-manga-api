from django.http import JsonResponse

from app.Enums.StatusEnum import CustomerStatusEnum
from app.Services.LocalTime import localTime


class CustomerCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for customer in self.data["data"]:
            data.append(
                {
                    "id": customer.id,
                    "email": customer.email,
                    "nick_name": customer.nick_name,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "total_story": customer.story_set.count(),
                    "status": customer.status,
                    "created_at": localTime(customer.created_at),
                    "updated_at": localTime(customer.updated_at),
                }
            )
        self.data["data"] = data
        return self.data

    def getStatus(self, isActive: bool):
        if isActive:
            return CustomerStatusEnum.ACTIVE
        return CustomerStatusEnum.INACTIVE
