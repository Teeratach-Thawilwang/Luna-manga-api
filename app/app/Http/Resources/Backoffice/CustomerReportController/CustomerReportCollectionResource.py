from app.Services.LocalTime import localTime
from django.http import JsonResponse


class CustomerReportCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for customerReport in self.data["data"]:
            data.append(
                {
                    "id": customerReport.id,
                    "group": customerReport.group,
                    "source": customerReport.model_type.model,
                    "customer_id": customerReport.customer_id,
                    "is_accept": customerReport.is_accept,
                    "created_at": localTime(customerReport.created_at),
                    "updated_at": localTime(customerReport.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
