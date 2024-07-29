from app.Domain.Authentication.Models.OAuthAccessToken import OAuthAccessToken
from app.Domain.Authentication.Models.OAuthClientFactory import OAuthClientFactory
from django.utils import timezone
from factory import SubFactory
from factory.django import DjangoModelFactory


class OAuthAccessTokenFactory(DjangoModelFactory):
    scopes = "read write"
    created_at = timezone.now()
    updated_at = timezone.now()
    expired_at = timezone.now() + timezone.timedelta(days=7)
    revoked_at = None

    client = SubFactory(OAuthClientFactory)

    class Meta:
        model = OAuthAccessToken
