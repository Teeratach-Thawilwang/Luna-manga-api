from app.Domain.Widget.Models.Widget import Widget
from app.Domain.Widget.Services.WidgetService import WidgetService
from app.Enums.StatusEnum import BannerStatusEnum
from app.Services.Paginator import paginate
from django.db.models import Q
from django.http import JsonResponse


class WidgetCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for widget in self.data["data"]:
            data.append(
                {
                    "id": widget.id,
                    "sequence": widget.widgetsequence_set.first().sequence,
                    "title": widget.title,
                    "type": widget.type,
                    "banners": self.getBannersPaginated(widget),
                }
            )
        self.data["data"] = data
        return self.data

    def getBannersPaginated(self, widget: Widget):
        bannerPaginated = paginate(1, 15, widget.widgetbanner_set, [Q(banner__status=BannerStatusEnum.ACTIVE)])
        bannerPaginated["data"] = WidgetService().transformBannersFromWidgetBanners(bannerPaginated["data"])
        return bannerPaginated
