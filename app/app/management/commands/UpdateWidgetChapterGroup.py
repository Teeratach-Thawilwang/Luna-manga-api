from django.core.management.base import BaseCommand
from django.db.models import IntegerField, Max, OuterRef, Subquery
from django.db.models.functions import Cast, Substr

from app.Domain.Banner.Models.Banner import Banner
from app.Domain.Widget.Services.WidgetService import WidgetService
from app.Enums.BannerTypeEnum import BannerTypeEnum
from app.Enums.StatusEnum import WidgetStatusEnum
from app.Enums.WidgetTypeEnum import WidgetTypeEnum

"""
To run command
shell  run => python manage.py UpdateWidgetChapterGroup
docker run => docker-compose exec app python manage.py UpdateWidgetChapterGroup
"""


class Command(BaseCommand):
    help = f"Update widget type={WidgetTypeEnum.CHAPTER_GROUP}."

    def handle(self, *args, **kwargs):
        # Group by story
        # subquery = Banner.objects.filter(type=BannerTypeEnum.CHAPTER).values("title").annotate(max_id=Max("id")).values("max_id")
        # bannerIdsDict = Banner.objects.filter(id__in=subquery, type=BannerTypeEnum.CHAPTER).order_by("-id").values("id")

        # No Group by
        # bannerIdsDict = Banner.objects.filter(type=BannerTypeEnum.CHAPTER).order_by("-id").values("id")[:100]

        # Group by story, sort by banner name
        maxNameNumberSubquery = (
            Banner.objects.filter(type=BannerTypeEnum.CHAPTER, title=OuterRef("title"))
            .annotate(name_number=Cast(Substr("name", 7), IntegerField()))
            .values("title")
            .annotate(max_name_number=Max("name_number"))
            .values("max_name_number")
        )
        bannersWithMaxNameNumber = Banner.objects.annotate(name_number=Cast(Substr("name", 7), IntegerField())).filter(type=BannerTypeEnum.CHAPTER, name_number=Subquery(maxNameNumberSubquery))
        groupedBannersSubquery = bannersWithMaxNameNumber.values("title").annotate(max_id=Max("id")).values("max_id")
        bannerIdsDict = Banner.objects.filter(id__in=Subquery(groupedBannersSubquery), type=BannerTypeEnum.CHAPTER).order_by("-id").values("id")

        bannerIds = [banner["id"] for banner in bannerIdsDict]

        widgetService = WidgetService()
        widgetChapter = widgetService.findBy({"type": WidgetTypeEnum.CHAPTER_GROUP}).first()

        if widgetChapter != None:
            params = {
                "id": widgetChapter.id,
                "name": widgetChapter.name,
                "title": widgetChapter.title,
                "type": widgetChapter.type,
                "status": widgetChapter.status,
                "banner_ids": bannerIds,
                "updated_by_id": 1,
            }
            widgetService.update(widgetChapter.id, params)
        else:
            params = {
                "name": "ตอนใหม่ล่าสุด",
                "title": "ตอนใหม่ล่าสุด",
                "type": WidgetTypeEnum.CHAPTER_GROUP,
                "status": WidgetStatusEnum.ACTIVE,
                "banner_ids": bannerIds,
                "updated_by_id": 1,
            }
            widgetService.create(params)

        print(f"Update widget type={WidgetTypeEnum.CHAPTER_GROUP} successfully.")
