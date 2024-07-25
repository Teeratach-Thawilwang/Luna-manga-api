from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers


class UpdateRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["first_name"] = serializers.CharField(required=True)
        self.fields["last_name"] = serializers.CharField(required=True)
        self.fields["nick_name"] = serializers.CharField(required=True)
        self.fields["profile_image_id"] = serializers.IntegerField(required=False)

        super().__init__(instance, data, **kwargs)
