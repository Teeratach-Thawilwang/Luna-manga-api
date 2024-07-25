from app.Domain.Category.Models.Category import Category
from app.Enums.StatusEnum import CategoryStatusEnum
from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers


class UpdateRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["id"] = serializers.IntegerField(required=True)
        self.fields["name"] = serializers.CharField(required=True)
        self.fields["type"] = serializers.CharField(required=True)
        self.fields["status"] = serializers.ChoiceField([CategoryStatusEnum.ACTIVE, CategoryStatusEnum.INACTIVE], required=True)

        super().__init__(instance, data, **kwargs)

    def validate(self, data):
        data = dict(data)
        if {"id", "name", "type"}.issubset(data):
            id = data["id"]
            name = data["name"]
            type = data["type"]

        if Category.objects.filter(name=name, type=type).exclude(pk=id).exists():
            raise serializers.ValidationError({"name": "Category name and type already exist."})

        return data
