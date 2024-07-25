from app.Domain.Story.Models.Story import Story
from app.Enums.CategoryEnum import CategoryEnum
from factory import Faker
from factory.django import DjangoModelFactory
from app.Enums.StatusEnum import StoryStatusEnum


class StoryFactory(DjangoModelFactory):
    customer_id = 1
    slug = Faker("slug")
    name = Faker("name")
    description = Faker("text", max_nb_chars=100)
    type = Faker("random_element", elements=CategoryEnum.list())
    status = Faker("random_element", elements=StoryStatusEnum.list())
    view_count = Faker('random_int', min=1, max=100)
    
    class Meta:
        model = Story
