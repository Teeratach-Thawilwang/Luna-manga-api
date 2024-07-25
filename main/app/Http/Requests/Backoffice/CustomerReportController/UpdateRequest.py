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
        self.fields["is_accept"] = serializers.BooleanField(required=True)

        super().__init__(instance, data, **kwargs)
