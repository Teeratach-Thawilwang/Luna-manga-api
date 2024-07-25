from app.Domain.Banner.Models.Banner import Banner
from app.Enums.BannerTypeEnum import BannerTypeEnum
from app.Enums.StatusEnum import BannerStatusEnum
from factory import Faker
from factory.django import DjangoModelFactory


class BannerFactory(DjangoModelFactory):
    name = Faker("domain_word")
    title = Faker("domain_word")
    type = Faker("random_element", elements=BannerTypeEnum.list())
    link = Faker("uri")
    status = Faker("random_element", elements=BannerStatusEnum.list())

    class Meta:
        model = Banner
