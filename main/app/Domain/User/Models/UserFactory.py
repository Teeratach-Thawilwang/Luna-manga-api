import random
import string

from app.Domain.User.Models.User import User
from app.Enums.StatusEnum import UserStatusEnum
from factory import Faker, LazyFunction
from factory.django import DjangoModelFactory


def generatePhoneNumber(length=10):
    return "".join(random.choices(string.digits, k=length))


class UserFactory(DjangoModelFactory):
    email = Faker("email")
    password = Faker("password")
    nick_name = Faker("first_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    phone_number = LazyFunction(lambda: generatePhoneNumber(length=10))
    status = Faker("random_element", elements=UserStatusEnum.list())
    is_superuser = False
    is_deleted = False

    class Meta:
        model = User
