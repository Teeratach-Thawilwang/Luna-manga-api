from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers


class IndexRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["page"] = serializers.ListField(child=serializers.IntegerField(), required=True)
        self.fields["per_page"] = serializers.ListField(child=serializers.IntegerField(), required=True)
        self.fields["order_by"] = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)

        super().__init__(instance, data, **kwargs)


class IntOrStrField(serializers.Field):
    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("This field should be a list.")

        for item in data:
            if not isinstance(item, (int, str)):
                raise serializers.ValidationError("All items in the list should be integer or string.")

        return data

    def to_representation(self, value):
        return value
