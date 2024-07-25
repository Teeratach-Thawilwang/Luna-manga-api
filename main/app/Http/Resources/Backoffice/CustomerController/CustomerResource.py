from app.Domain.Customer.Models.Customer import Customer
from app.Domain.File.Services.FileableService import FileableService
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Http.Resources.Backoffice.CustomerGroupController.CustomerGroupCollectionResource import CustomerGroupCollectionResource
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class CustomerResource(JsonResponse):
    def __init__(self, customer: Customer, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": customer.id,
            "email": customer.email,
            "nick_name": customer.nick_name,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "profile_image": FileableService().transformImagesByCollection(customer.fileable, CollectionNameEnum.PROFILE_IMAGE),
            "customer_group": CustomerGroupCollectionResource({"data": [customer.customer_group]}).data["data"][0],
            "status": customer.status,
            "created_at": localTime(customer.created_at),
            "updated_at": localTime(customer.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
