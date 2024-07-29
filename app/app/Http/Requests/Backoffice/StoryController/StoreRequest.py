from app.Domain.Story.Models.Story import Story
from app.Enums.CategoryEnum import CategoryEnum
from app.Enums.StatusEnum import StoryStatusEnum
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
        unique = UniqueValidator(queryset=Story.objects.all())

        self.fields["name"] = serializers.CharField(
            validators=[
                unique,
            ],
            required=True,
        )
        self.fields["slug"] = serializers.CharField(required=True)
        self.fields["description"] = serializers.CharField(required=True)
        self.fields["type"] = serializers.ChoiceField(CategoryEnum.list(), required=True)
        self.fields["status"] = serializers.ChoiceField(StoryStatusEnum.list(), required=True)
        self.fields["category_ids"] = serializers.ListField(child=serializers.IntegerField(), required=True)
        self.fields["cover_image_id"] = serializers.IntegerField(required=True)

        super().__init__(instance, data, **kwargs)
