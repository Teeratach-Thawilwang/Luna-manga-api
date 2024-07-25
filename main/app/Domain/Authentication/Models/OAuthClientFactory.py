from app.Domain.Authentication.Models.OAuthClient import OAuthClient
from factory import Faker
from factory.django import DjangoModelFactory


class OAuthClientFactory(DjangoModelFactory):
    name = Faker("company")
    client_id = Faker("uuid4")
    client_secret = Faker("uuid4")
    redirect_url = Faker("url")
    created_at = Faker("date_time_this_decade")
    updated_at = Faker("date_time_this_decade")

    class Meta:
        model = OAuthClient
