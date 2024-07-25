from app.Domain.CustomerGroup.Models.CustomerGroup import CustomerGroup
from factory import Faker
from factory.django import DjangoModelFactory


class CustomerGroupFactory(DjangoModelFactory):
    name = Faker("word")

    class Meta:
        model = CustomerGroup
