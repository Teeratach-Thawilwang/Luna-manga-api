from typing import Any

from app.Domain.WidgetSequence.Models.WidgetSequence import WidgetSequence
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from django.db.models.query import QuerySet
from django.utils import timezone


class WidgetSequenceService:
    def __init__(self):
        self.querySet = WidgetSequence.objects.prefetch_related("widget")

    def getAll(self) -> QuerySet:
        return self.querySet.order_by("sequence")

    def updateSequence(self, params: dict[str, Any]) -> WidgetSequence:
        widgetIds = None
        params["updated_at"] = timezone.now()

        if "widget_ids" in params:
            widgetIds = params["widget_ids"]

        try:
            if widgetIds != None:
                self.clearAll()
                self.createWidgetSequence(widgetIds)

            return self.getAll()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def clearAll(self):
        self.querySet.all().delete()

    def createWidgetSequence(self, widgetIds: list[int]):
        for i in range(len(widgetIds)):
            self.querySet.create(widget_id=widgetIds[i], sequence=(i + 1))
