from app.Domain.Authentication.Models.OAuthClient import OAuthClient
from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class StoreRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        UniqueOAuthClient = UniqueValidator(queryset=OAuthClient.objects.all())

        self.fields["name"] = serializers.CharField(validators=[UniqueOAuthClient], required=True, allow_null=False)
        self.fields["client_id"] = serializers.CharField(validators=[UniqueOAuthClient], required=False, allow_null=True)
        self.fields["client_secret"] = serializers.CharField(validators=[UniqueOAuthClient], required=False, allow_null=True)

        super().__init__(instance, data, **kwargs)
