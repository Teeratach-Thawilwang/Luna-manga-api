from app.Domain.Authorization.Models.Role import Role
from factory import Faker
from factory.django import DjangoModelFactory


class RoleFactory(DjangoModelFactory):
    guard_name = Faker("random_element", elements=["front-side", "backoffice"])
    name = Faker("name")
    description = Faker("name")

    class Meta:
        model = Role
