from app.Domain.CustomerGroup.Models.CustomerGroup import CustomerGroup
from django.conf import settings


class CustomerGroupSeeder:
    def create(self):
        groups = CustomerGroup.objects.values_list("name", flat=True)
        for group in settings.CUSTOMER_GROUPS_DEFAULT:
            if group["name"] not in groups:
                CustomerGroup.objects.create(**group)
