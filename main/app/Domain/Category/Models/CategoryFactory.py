from app.Domain.Category.Models.Category import Category
from app.Enums.CategoryEnum import CategoryEnum
from app.Enums.StatusEnum import CategoryStatusEnum
from factory import Faker
from factory.django import DjangoModelFactory


class CategoryFactory(DjangoModelFactory):
    name = Faker("name")
    type = Faker("random_element", elements=CategoryEnum.list())
    status = Faker("random_element", elements=CategoryStatusEnum.list())

    class Meta:
        model = Category
