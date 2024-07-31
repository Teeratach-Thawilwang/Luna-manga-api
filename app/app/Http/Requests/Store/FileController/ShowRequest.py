from app.Domain.User.Models.User import User
from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class ShowRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["conversion"] = serializers.ListField(child=serializers.CharField(), required=False)

        super().__init__(instance, data, **kwargs)
