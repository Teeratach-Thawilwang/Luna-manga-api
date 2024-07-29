from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Story.Models.Story import Story
from app.Enums.CategoryEnum import CategoryEnum
from app.Enums.StatusEnum import ChapterStatusEnum
from app.Exceptions.ValidationException import ValidationException
from rest_framework import serializers


class StoreRequest:
    def __init__(self, request):
        validator = Validator(data=request.params)
        if not validator.is_valid():
            raise ValidationException(validator.errors)


class Validator(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["story_id"] = serializers.IntegerField(required=True)
        self.fields["name"] = serializers.CharField(required=True)
        self.fields["chapter_number"] = serializers.IntegerField(required=True)
        self.fields["type"] = serializers.ChoiceField(CategoryEnum.list(), required=True)
        self.fields["status"] = serializers.ChoiceField(ChapterStatusEnum.list(), required=True)
        self.fields["text"] = serializers.CharField(required=True)
        self.fields["cover_image_id"] = serializers.IntegerField(required=True)

        super().__init__(instance, data, **kwargs)

    def validate(self, data):
        data = dict(data)
        if {"story_id", "name"}.issubset(data):
            storyId = data["story_id"]
            chapterType = data["type"]
            chapterNumber = data["chapter_number"]

            story = Story.objects.get(pk=storyId)
            if chapterType != story.type:
                raise serializers.ValidationError({"type": "Type is not corresponding to story type."})

            if Chapter.objects.filter(story_id=storyId, chapter_number=chapterNumber).exists():
                raise serializers.ValidationError({"chapter_number": "Chapter number already exist."})

        return data
