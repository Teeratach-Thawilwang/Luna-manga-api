from rest_framework import status, viewsets

from app.Domain.WidgetSequence.Services.WidgetSequenceService import WidgetSequenceService
from app.Enums.CachePagePrefixEnum import CachePagePrefixEnum
from app.Http.Requests.Backoffice.WidgetSequenceController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.WidgetSequenceController.WidgetSequenceCollectionResource import WidgetSequenceCollectionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from app.Services.Helpers import clearAllRedisCacheByKeyPrefix


class WidgetSequenceController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "update"]
        request.permissions = {
            "widget.view": ["index"],
            "widget.manage": ["update"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        widgetSequence = WidgetSequenceService().getAll()
        return WidgetSequenceCollectionResource({"data": widgetSequence})

    def update(self, request):
        UpdateRequest(request)

        params = request.params
        widgetSequence = WidgetSequenceService().updateSequence(params)
        clearAllRedisCacheByKeyPrefix(CachePagePrefixEnum.STORE_WIDGET_INDEX)
        clearAllRedisCacheByKeyPrefix(CachePagePrefixEnum.STORE_WIDGET_ON_PAGE)
        clearAllRedisCacheByKeyPrefix(CachePagePrefixEnum.STORE_WIDGET_BANNER)
        clearAllRedisCacheByKeyPrefix(CachePagePrefixEnum.PRESIGNED_URL)

        return WidgetSequenceCollectionResource({"data": widgetSequence})
