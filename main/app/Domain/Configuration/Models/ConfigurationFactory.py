import factory
from app.Domain.Configuration.Models.Configuration import Configuration
from factory.django import DjangoModelFactory


class ConfigurationFactory(DjangoModelFactory):
    key = factory.Faker("word")
    value = factory.Faker("word")

    class Meta:
        model = Configuration
