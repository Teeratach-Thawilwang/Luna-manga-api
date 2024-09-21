from rest_framework import serializers

from app.Enums.CollectionEnum import CollectionNameEnum
from app.Exceptions.ValidationException import ValidationException


class StoreRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["file"] = serializers.ListField(child=serializers.FileField(), required=True)
        self.fields["collection_name"] = serializers.ChoiceField(CollectionNameEnum.list(), required=True)
        self.fields["is_sync"] = serializers.BooleanField(required=False)

        super().__init__(instance, data, **kwargs)
