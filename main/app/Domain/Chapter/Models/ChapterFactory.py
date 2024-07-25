from app.Domain.Chapter.Models.Chapter import Chapter
from app.Enums.CategoryEnum import CategoryEnum
from app.Enums.StatusEnum import ChapterStatusEnum
from factory import Faker
from factory.django import DjangoModelFactory


class ChapterFactory(DjangoModelFactory):
    name = Faker("name")
    chapter_number = Faker("random_int", min=1, max=100)
    type = Faker("random_element", elements=CategoryEnum.list())
    status = Faker("random_element", elements=ChapterStatusEnum.list())

    class Meta:
        model = Chapter
