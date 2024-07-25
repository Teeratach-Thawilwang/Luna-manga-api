from app.Domain.User.Models.User import User
from app.Enums.StatusEnum import UserStatusEnum
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
        unique = UniqueValidator(queryset=User.objects.all().exclude(pk=id))

        self.fields["id"] = serializers.IntegerField(required=True)
        self.fields["email"] = serializers.EmailField(
            validators=[
                unique,
            ],
            required=True,
        )
        self.fields["password"] = serializers.CharField(min_length=8, required=False)
        self.fields["nick_name"] = serializers.CharField(required=True)
        self.fields["first_name"] = serializers.CharField(required=True)
        self.fields["last_name"] = serializers.CharField(required=True)
        self.fields["status"] = serializers.ChoiceField(UserStatusEnum.list(), required=True)

        super().__init__(instance, data, **kwargs)
