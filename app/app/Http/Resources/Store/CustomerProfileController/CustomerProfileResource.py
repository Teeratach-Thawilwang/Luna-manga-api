from django.http import JsonResponse

from app.Domain.Customer.Models.Customer import Customer
from app.Domain.File.Services.FileableService import FileableService
from app.Enums.CollectionEnum import CollectionNameEnum


class CustomerProfileResource(JsonResponse):
    def __init__(self, customer: Customer, status=200, safe=False, json_dumps_params=None, **kwargs):
        customer = Customer.objects.filter(id=customer.id)
        customer = customer.prefetch_related("fileable__file")
        customer = customer.first()

        self.data = {
            "id": customer.id,
            "email": customer.email,
            "nick_name": customer.nick_name,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "profile_image": FileableService().transformImagesByCollection(customer.fileable.all(), CollectionNameEnum.PROFILE_IMAGE, "store"),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
