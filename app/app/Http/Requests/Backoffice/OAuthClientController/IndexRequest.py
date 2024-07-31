from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers


class IndexRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["q"] = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)
        self.fields["page"] = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)
        self.fields["per_page"] = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)
        self.fields["order_by"] = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)

        super().__init__(instance, data, **kwargs)
