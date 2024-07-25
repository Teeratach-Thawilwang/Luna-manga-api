from app.Domain.CustomerGroup.Models.CustomerGroup import CustomerGroup
from app.Enums.StatusEnum import CustomerGroupStatusEnum
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
        unique = UniqueValidator(queryset=CustomerGroup.objects.all().exclude(pk=id))

        self.fields["id"] = serializers.IntegerField(required=True)
        self.fields["name"] = serializers.CharField(
            validators=[
                unique,
            ],
            required=True,
        )
        self.fields["status"] = serializers.ChoiceField([CustomerGroupStatusEnum.ACTIVE, CustomerGroupStatusEnum.INACTIVE], required=True)

        super().__init__(instance, data, **kwargs)
