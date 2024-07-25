from app.Domain.Customer.Models.Customer import Customer
from app.Enums.StatusEnum import CustomerStatusEnum
from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UpdateRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        id = data["id"]
        UniqueCustomer = UniqueValidator(queryset=Customer.objects.all().exclude(pk=id))

        self.fields["id"] = serializers.IntegerField(required=True)
        self.fields["email"] = serializers.EmailField(
            validators=[
                UniqueCustomer,
            ],
            required=True,
        )
        self.fields["nick_name"] = serializers.CharField(required=True)
        self.fields["first_name"] = serializers.CharField(required=True)
        self.fields["last_name"] = serializers.CharField(required=True)
        self.fields["status"] = serializers.ChoiceField([CustomerStatusEnum.ACTIVE, CustomerStatusEnum.INACTIVE], required=True)
        self.fields["profile_image_id"] = serializers.IntegerField(required=True)
        self.fields["customer_group_id"] = serializers.IntegerField(required=True)

        super().__init__(instance, data, **kwargs)
