from app.Domain.Authentication.Models.OAuthClient import OAuthClient
from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RefreshTokenRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["refresh_token"] = serializers.CharField(required=True, allow_null=False)
        super().__init__(instance, data, **kwargs)
