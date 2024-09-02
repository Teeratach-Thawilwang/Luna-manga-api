import django.db.models.query
from django.db.models import Min, Q
from django.db.models.query import QuerySet
from django.http import JsonResponse

from app.Domain.Widget.Models.Widget import Widget
from app.Domain.Widget.Services.WidgetService import WidgetService
from app.Enums.StatusEnum import BannerStatusEnum
from app.Services.Paginator import paginate


class WidgetCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        widgets: QuerySet[Widget] = self.data["data"].prefetch_related("widgetsequence_set")
        widgets = widgets.annotate(first_sequence=Min("widgetsequence__sequence"))
        for widget in widgets:
            data.append(
                {
                    "id": widget.id,
                    "sequence": widget.first_sequence,
                    "title": widget.title,
                    "type": widget.type,
                    "banners": self.getBannersPaginated(widget),
                }
            )
        self.data["data"] = data
        return self.data

    def getBannersPaginated(self, widget: Widget):
        query = [Q(banner__status=BannerStatusEnum.ACTIVE)]
        orderBy = ["id"]
        widgetBannerPaginated = paginate(1, 15, widget.widgetbanner_set, query, orderBy)
        widgetBanners = widgetBannerPaginated["data"].prefetch_related("banner__fileable__file")
        widgetBannerPaginated["data"] = WidgetService().transformBannersFromWidgetBanners(widgetBanners)
        return widgetBannerPaginated
