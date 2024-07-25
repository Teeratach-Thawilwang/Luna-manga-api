from app.Enums.CustomerReportGroupEnum import CustomerReportGroupEnum
from app.Enums.CustomerReportSourceEnum import CustomerReportSourceEnum
from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers


class StoreRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["group"] = serializers.ChoiceField(CustomerReportGroupEnum.list(), required=True)
        self.fields["source"] = serializers.ChoiceField(CustomerReportSourceEnum.list(), required=True)
        self.fields["model_id"] = serializers.IntegerField(required=True)
        self.fields["customer_id"] = serializers.IntegerField(required=True)
        self.fields["message"] = serializers.CharField(allow_blank=True, required=True)

        super().__init__(instance, data, **kwargs)
