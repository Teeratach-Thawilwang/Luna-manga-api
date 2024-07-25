from app.Domain.Widget.Models.Widget import Widget
from app.Domain.Widget.Services.WidgetService import WidgetService
from app.Enums.StatusEnum import BannerStatusEnum
from app.Services.Paginator import paginate
from django.db.models import Q
from django.http import JsonResponse


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
        bannerPaginated = paginate(page, perPage, widget.widgetbanner_set, [Q(banner__status=BannerStatusEnum.ACTIVE)])
        bannerPaginated["data"] = WidgetService().transformBannersFromWidgetBanners(bannerPaginated["data"])
        return bannerPaginated
