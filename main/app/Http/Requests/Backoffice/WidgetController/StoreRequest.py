from app.Domain.Banner.Models.Banner import Banner
from app.Domain.Widget.Models.Widget import Widget
from app.Enums.BannerTypeEnum import BannerTypeEnum
from app.Enums.StatusEnum import WidgetStatusEnum
from app.Enums.WidgetTypeEnum import WidgetTypeEnum
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
        unique = UniqueValidator(queryset=Widget.objects.all())

        self.fields["name"] = serializers.CharField(validators=[unique], required=True)
        self.fields["title"] = serializers.CharField(required=True)
        self.fields["type"] = serializers.ChoiceField(WidgetTypeEnum.list(), required=True)
        self.fields["status"] = serializers.ChoiceField(WidgetStatusEnum.list(), required=True)
        self.fields["banner_ids"] = serializers.ListField(child=serializers.IntegerField(), min_length=1)

        super().__init__(instance, data, **kwargs)

    def validate(self, data):
        data = dict(data)
        if {"type", "banner_ids"}.issubset(data):
            type = data["type"]
            bannerIds = data["banner_ids"]

            bannerTypes = Banner.objects.filter(id__in=bannerIds).distinct().values_list("type")
            bannerTypes = [item[0] for item in bannerTypes]

            if len(bannerTypes) > 1:
                raise serializers.ValidationError({"banner_ids": "banner type not match with widget type."})

            match type:
                case WidgetTypeEnum.STORY_LIST:
                    self.validateType(bannerTypes, BannerTypeEnum.STORY)
                case WidgetTypeEnum.STORY_GROUP:
                    self.validateType(bannerTypes, BannerTypeEnum.STORY)
                case WidgetTypeEnum.CHAPTER_GROUP:
                    self.validateType(bannerTypes, BannerTypeEnum.CHAPTER)
                case WidgetTypeEnum.STORY_WINDOW:
                    self.validateType(bannerTypes, BannerTypeEnum.STORY_WINDOW)
                case WidgetTypeEnum.ADVERTISEMENT_SMALL:
                    self.validateType(bannerTypes, BannerTypeEnum.ADVERTISEMENT_SMALL)
                case WidgetTypeEnum.ADVERTISEMENT_MEDIUM:
                    self.validateType(bannerTypes, BannerTypeEnum.ADVERTISEMENT_MEDIUM)
                case WidgetTypeEnum.ADVERTISEMENT_GROUP:
                    self.validateType(bannerTypes, BannerTypeEnum.ADVERTISEMENT_GROUP)

        return data

    def validateType(self, bannerTypes: list[str], expectType: BannerTypeEnum):
        if expectType in bannerTypes:
            return
        raise serializers.ValidationError({"banner_ids": "banner type not match with widget type."})
