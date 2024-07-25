from app.Domain.Banner.Models.Banner import Banner
from app.Domain.Banner.Services.BannerService import BannerService
from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Story.Models.Story import Story
from app.Enums.BannerTypeEnum import BannerTypeEnum
from app.Http.Resources.Backoffice.ChapterController.ChapterCollectionResource import ChapterCollectionResource
from app.Http.Resources.Backoffice.StoryController.StoryCollectionResource import StoryCollectionResource
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class BannerResource(JsonResponse):
    def __init__(self, banner: Banner, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": banner.id,
            "name": banner.name,
            "title": banner.title,
            "type": banner.type,
            "link": banner.link,
            "status": banner.status,
            "story": self.getStory(banner),
            "chapter": self.getChapter(banner),
            "images": BannerService().transformBannerImages(banner, "backoffice"),
            "created_at": localTime(banner.created_at),
            "updated_at": localTime(banner.updated_at),
            "updated_by": self.getUpdatedBy(banner),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def getStory(self, banner: Banner):
        if banner.type != BannerTypeEnum.STORY:
            return None

        story = Story.objects.get(pk=banner.model_id)
        return StoryCollectionResource({"data": [story]}).data["data"][0]

    def getChapter(self, banner: Banner):
        if banner.type != BannerTypeEnum.CHAPTER:
            return None

        chapter = Chapter.objects.get(pk=banner.model_id)
        return ChapterCollectionResource({"data": [chapter]}).data["data"][0]

    def getUpdatedBy(self, banner: Banner):
        if banner.updated_by == None:
            return ""

        user = banner.updated_by
        return f"{user.first_name} {user.last_name} (id={user.id})"
