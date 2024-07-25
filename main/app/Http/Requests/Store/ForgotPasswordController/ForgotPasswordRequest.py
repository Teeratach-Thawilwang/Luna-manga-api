from app.Domain.Customer.Models.Customer import Customer
from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class ForgotPasswordRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["email"] = serializers.EmailField(required=True)

        super().__init__(instance, data, **kwargs)
