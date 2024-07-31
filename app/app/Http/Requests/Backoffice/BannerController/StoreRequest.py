from app.Domain.Banner.Models.Banner import Banner
from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Story.Models.Story import Story
from app.Enums.BannerTypeEnum import BannerTypeEnum
from app.Enums.StatusEnum import BannerStatusEnum
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
        unique = UniqueValidator(queryset=Banner.objects.all())

        self.fields["name"] = serializers.CharField(validators=[unique], required=True)
        self.fields["title"] = serializers.CharField(required=True)
        self.fields["type"] = serializers.ChoiceField(BannerTypeEnum.list(), required=True)
        self.fields["link"] = serializers.CharField(required=True)
        self.fields["status"] = serializers.ChoiceField(BannerStatusEnum.list(), required=True)
        self.fields["story_id"] = serializers.IntegerField(allow_null=True, required=False)
        self.fields["chapter_id"] = serializers.IntegerField(allow_null=True, required=False)
        self.fields["image_ids"] = serializers.ListField(child=serializers.IntegerField())

        super().__init__(instance, data, **kwargs)

    def validate(self, data):
        data = dict(data)
        if {"type"}.issubset(data):
            type = data["type"]

            match type:
                case BannerTypeEnum.CHAPTER:
                    self.validateTypeChapter(data)
                case BannerTypeEnum.STORY:
                    self.validateTypeStory(data)
                case BannerTypeEnum.STORY_WINDOW:
                    self.validateTypeStoryWindow(data)
                case BannerTypeEnum.ADVERTISEMENT_SMALL:
                    self.validateTypeAdvertisement(data)
                case BannerTypeEnum.ADVERTISEMENT_MEDIUM:
                    self.validateTypeAdvertisement(data)
                case BannerTypeEnum.ADVERTISEMENT_GROUP:
                    self.validateTypeAdvertisement(data)

        return data

    def validateTypeChapter(self, data):
        if not {"chapter_id"}.issubset(data):
            raise serializers.ValidationError({"chapter_id": "chapter_id is required for banner type Chapter."})

        chapterId = data["chapter_id"]
        if not Chapter.objects.filter(id=chapterId).exists():
            raise serializers.ValidationError({"chapter_id": "Resource not found."})

    def validateTypeStory(self, data):
        if not {"story_id"}.issubset(data):
            raise serializers.ValidationError({"story_id": "story_id is required for banner type Story."})

        storyId = data["story_id"]
        if not Story.objects.filter(id=storyId).exists():
            raise serializers.ValidationError({"story_id": "Resource not found."})

    def validateTypeStoryWindow(self, data):
        self.validateImageIdsLength(data, 3)

    def validateTypeAdvertisement(self, data):
        self.validateImageIdsLength(data, 1)

    def validateImageIdsLength(self, data, number):
        if not {"image_ids"}.issubset(data):
            raise serializers.ValidationError({"image_ids": f"Require {number} image id."})

        imageIds = data["image_ids"]
        if len(imageIds) != number:
            raise serializers.ValidationError({"image_ids": f"Require {number} image id."})
