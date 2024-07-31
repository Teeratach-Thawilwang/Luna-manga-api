from app.Domain.Widget.Models.Widget import Widget
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class WidgetSequenceCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for widgetSequence in self.data["data"]:
            widget: Widget = widgetSequence.widget
            data.append(
                {
                    "id": widget.id,
                    "sequence": widgetSequence.sequence,
                    "name": widget.name,
                    "total_banner": widget.widgetbanner_set.count(),
                    "type": widget.type,
                    "status": widget.status,
                    "created_at": localTime(widget.created_at),
                    "updated_at": localTime(widget.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
