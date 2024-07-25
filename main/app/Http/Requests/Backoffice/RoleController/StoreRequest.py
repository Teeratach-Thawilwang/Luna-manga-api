from app.Domain.Authorization.Models.Role import Role
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
        UniqueRole = UniqueValidator(queryset=Role.objects.all())

        self.fields["name"] = serializers.CharField(
            validators=[
                UniqueRole,
            ],
            required=True,
        )
        self.fields["guard_name"] = serializers.CharField(required=False)
        self.fields["description"] = serializers.CharField(required=True, allow_blank=True)
        self.fields["user_ids"] = serializers.ListField(child=serializers.IntegerField())
        self.fields["permission_ids"] = serializers.ListField(child=serializers.IntegerField())

        super().__init__(instance, data, **kwargs)
