from app.Enums.StatusEnum import CustomerGroupStatusEnum
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class CustomerGroupCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for customerGroup in self.data["data"]:
            data.append(
                {
                    "id": customerGroup.id,
                    "name": customerGroup.name,
                    "total_customer": customerGroup.customer_set.count(),
                    "status": customerGroup.status,
                    "created_at": localTime(customerGroup.created_at),
                    "updated_at": localTime(customerGroup.updated_at),
                }
            )
        self.data["data"] = data
        return self.data

    def getStatus(self, isActive: bool):
        if isActive:
            return CustomerGroupStatusEnum.ACTIVE
        return CustomerGroupStatusEnum.INACTIVE
