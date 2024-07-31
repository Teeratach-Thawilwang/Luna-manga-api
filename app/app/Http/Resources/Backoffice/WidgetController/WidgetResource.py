from app.Domain.Widget.Models.Widget import Widget
from app.Domain.Widget.Services.WidgetService import WidgetService
from app.Http.Resources.Backoffice.BannerController.BannerCollectionResource import BannerCollectionResource
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class WidgetResource(JsonResponse):
    def __init__(self, widget: Widget, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": widget.id,
            "name": widget.name,
            "title": widget.title,
            "type": widget.type,
            "status": widget.status,
            "banners": self.getBanners(widget),
            "created_at": localTime(widget.created_at),
            "updated_at": localTime(widget.updated_at),
            "updated_by": self.getUpdatedBy(widget),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def getBanners(self, widget: Widget):
        banners = WidgetService().getBanners(widget)
        return BannerCollectionResource({"data": banners}).data["data"]

    def getUpdatedBy(self, widget: Widget):
        if widget.updated_by == None:
            return ""

        user = widget.updated_by
        return f"{user.first_name} {user.last_name} (id={user.id})"
