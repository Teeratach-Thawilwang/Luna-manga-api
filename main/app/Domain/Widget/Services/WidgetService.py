from sys import modules
from typing import Any

from app.Domain.Banner.Models.Banner import Banner
from app.Domain.Widget.Models.Widget import Widget
from app.Domain.Widget.Models.WidgetBanner import WidgetBanner
from app.Domain.WidgetSequence.Models.WidgetSequence import WidgetSequence
from app.Enums.StatusEnum import WidgetStatusEnum
from app.Enums.WidgetTypeEnum import WidgetTypeEnum
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate
from django.db.models import Q, Subquery
from django.db.models.query import QuerySet
from django.utils import timezone

if "BannerService" not in modules:
    from app.Domain.Banner.Services.BannerService import BannerService


class WidgetService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id", "name"]
        self.querySet = Widget.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id) -> Widget:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Widget:
        bannerIds = None
        if "banner_ids" in params:
            bannerIds = params["banner_ids"]
            del params["banner_ids"]

        widget = self.querySet.create(**params)
        if bannerIds != None:
            self.syncBanner(widget.id, bannerIds)

        return widget

    def update(self, id: int, params: dict[str, Any]) -> Widget:
        bannerIds = None
        params["updated_at"] = timezone.now()

        if "banner_ids" in params:
            bannerIds = params["banner_ids"]
            del params["banner_ids"]

        try:
            self.querySet.filter(pk=id).update(**params)
            widget = self.querySet.get(pk=id)

            if bannerIds != None:
                self.syncBanner(id, bannerIds)

            return widget
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteById(self, id) -> None:
        try:
            widget = self.querySet.get(pk=id)
            widget.delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def prefetch(self, *relations: tuple):
        self.querySet = self.querySet.prefetch_related(*relations)
        return self

    def search(self, params):
        if "q" in params:
            q: str = params["q"][0]
            if q.isnumeric():
                self.query += [Q(id__exact=q)]
            else:
                self.query += [Q(name__startswith=q)]

        if "status" in params:
            self.query += [Q(status__exact=params["status"][0])]

        if "type" in params:
            self.query += [Q(type__exact=params["type"][0])]

        if "start_date" in params:
            self.query += [Q(created_at__gte=params["start_date"][0])]

        if "end_date" in params:
            self.query += [Q(created_at__lte=params["end_date"][0])]

        if "page" in params:
            self.page = int(params["page"][0])

        if "per_page" in params:
            self.perPage = int(params["per_page"][0])

        if "order_by" in params:
            self.orderBy = params["order_by"]

        # For front-side
        if "in_widget_sequence" in params:
            if params["in_widget_sequence"]:
                widgetIds = WidgetSequence.objects.values("widget_id")
                self.query += [Q(id__in=Subquery(widgetIds))]

        if "types[]" in params:
            types = params["types[]"]
            self.query += [Q(type__in=types)]

        return self

    def paginate(self) -> list:
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)

    def syncBanner(self, widgetId: int, bannerIds: list[int]) -> None:
        WidgetBanner.objects.filter(widget_id=widgetId).delete()

        for bannerId in bannerIds:
            WidgetBanner.objects.create(widget_id=widgetId, banner_id=bannerId)

    def isActive(self, widget: Widget):
        return widget.status == WidgetStatusEnum.ACTIVE

    def getBanners(self, widget: Widget) -> list[Banner]:
        banners = []
        widgetBanners = widget.widgetbanner_set.prefetch_related("banner").order_by("id")
        for widgetBanner in widgetBanners:
            banners.append(widgetBanner.banner)

        return banners

    def transformBannersFromWidgetBanners(self, widgetBanners: list[WidgetBanner]):
        data = []
        bannerService = BannerService()
        for widgetBanner in widgetBanners:
            banner: Banner = widgetBanner.banner
            data.append(
                {
                    "id": banner.id,
                    "name": banner.name,
                    "title": banner.title,
                    "type": banner.type,
                    "link": banner.link,
                    "images": bannerService.transformBannerImages(banner, "store"),
                }
            )
        return data

    def transformWidgetOnPage(self, widget: Widget) -> dict[str, any]:
        return {
            "id": widget.id,
            "sequence": widget.widgetsequence_set.first().sequence,
            "title": widget.title,
            "type": widget.type,
            "banners": self.transformBannersFromWidgetBanners(widget.widgetbanner_set.all()),
        }

    def getWidgetOnPage(self) -> list[Widget]:
        widgetIds = WidgetSequence.objects.values("widget_id")
        querySet = [Q(status__exact=WidgetStatusEnum.ACTIVE), Q(id__in=Subquery(widgetIds))]
        types = [
            WidgetTypeEnum.ADVERTISEMENT_GROUP,
            WidgetTypeEnum.ADVERTISEMENT_MEDIUM,
            WidgetTypeEnum.ADVERTISEMENT_SMALL,
            WidgetTypeEnum.STORY_LIST,
            WidgetTypeEnum.STORY_WINDOW,
            WidgetTypeEnum.STORY_GROUP,
        ]
        widgets: list[Widget] = []

        for type in types:
            widget = Widget.objects.filter(*querySet, type=type).order_by("widgetsequence__sequence").first()
            if widget == None:
                continue
            widgets.append(self.transformWidgetOnPage(widget))

        return widgets
