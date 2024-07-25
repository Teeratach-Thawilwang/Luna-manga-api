from app.Domain.File.Models.File import File
from factory import Faker
from factory.django import DjangoModelFactory


class FileFactory(DjangoModelFactory):
    file_name = Faker("file_name")
    content_type = Faker("mime_type")
    collection_name = Faker("word")
    conversion = Faker("text")

    class Meta:
        model = File
