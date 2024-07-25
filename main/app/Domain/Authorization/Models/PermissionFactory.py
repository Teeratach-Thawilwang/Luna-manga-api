from app.Domain.Authorization.Models.Permission import Permission
from factory import Faker
from factory.django import DjangoModelFactory


class PermissionFactory(DjangoModelFactory):
    name = Faker("name")
    guard_name = Faker("random_element", elements=["front-side", "backoffice"])

    class Meta:
        model = Permission
