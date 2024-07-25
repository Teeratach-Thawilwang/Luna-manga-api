from app.Domain.Customer.Models.Customer import Customer
from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        UniqueCustomer = UniqueValidator(queryset=Customer.objects.all())

        self.fields["email"] = serializers.EmailField(
            validators=[
                UniqueCustomer,
            ],
            required=True,
        )
        self.fields["password"] = serializers.CharField(min_length=8, required=True)
        self.fields["first_name"] = serializers.CharField(required=True)
        self.fields["last_name"] = serializers.CharField(required=True)
        self.fields["nick_name"] = serializers.CharField(max_length=20, required=True)

        super().__init__(instance, data, **kwargs)
