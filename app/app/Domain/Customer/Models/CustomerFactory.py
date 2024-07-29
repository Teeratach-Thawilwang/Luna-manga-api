import random
import string

from app.Domain.Customer.Models.Customer import Customer
from app.Enums.StatusEnum import CustomerStatusEnum
from factory import Faker, LazyFunction
from factory.django import DjangoModelFactory


def generatePhoneNumber(length=10):
    return "".join(random.choices(string.digits, k=length))


class CustomerFactory(DjangoModelFactory):
    email = Faker("email")
    password = Faker("password")
    nick_name = Faker("name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    phone_number = LazyFunction(lambda: generatePhoneNumber(length=10))
    status = Faker("random_element", elements=CustomerStatusEnum.list())
    is_deleted = False

    class Meta:
        model = Customer
