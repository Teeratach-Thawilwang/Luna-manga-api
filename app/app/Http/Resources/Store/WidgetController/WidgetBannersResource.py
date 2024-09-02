from django.db.models import Q
from django.http import JsonResponse

from app.Domain.Widget.Models.Widget import Widget
from app.Domain.Widget.Services.WidgetService import WidgetService
from app.Enums.StatusEnum import BannerStatusEnum
from app.Services.Paginator import paginate


class WidgetBannersResource(JsonResponse):
    def __init__(self, widget: Widget, page: int, perPage: int, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": widget.id,
            "sequence": widget.widgetsequence_set.first().sequence,
            "title": widget.title,
            "type": widget.type,
            "banners": self.getBannersPaginated(widget, page, perPage),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def getBannersPaginated(self, widget: Widget, page: int, perPage: int):
        query = [Q(banner__status=BannerStatusEnum.ACTIVE)]
        orderBy = ["id"]
        widgetBannerPaginated = paginate(page, perPage, widget.widgetbanner_set, query, orderBy)
        widgetBanners = widgetBannerPaginated["data"].prefetch_related("banner__fileable__file")
        widgetBannerPaginated["data"] = WidgetService().transformBannersFromWidgetBanners(widgetBanners)
        return widgetBannerPaginated
