from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers


class UpdateRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["customer_id"] = serializers.IntegerField(required=True)
        self.fields["story_id"] = serializers.IntegerField(required=True)
        self.fields["like"] = serializers.IntegerField(required=False)
        self.fields["dislike"] = serializers.IntegerField(required=False)

        super().__init__(instance, data, **kwargs)
