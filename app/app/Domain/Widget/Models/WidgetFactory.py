from app.Domain.Widget.Models.Widget import Widget
from app.Enums.StatusEnum import WidgetStatusEnum
from app.Enums.WidgetTypeEnum import WidgetTypeEnum
from factory import Faker
from factory.django import DjangoModelFactory


class WidgetFactory(DjangoModelFactory):
    name = Faker("domain_word")
    title = Faker("domain_word")
    type = Faker("random_element", elements=WidgetTypeEnum.list())
    status = Faker("random_element", elements=WidgetStatusEnum.list())

    class Meta:
        model = Widget
