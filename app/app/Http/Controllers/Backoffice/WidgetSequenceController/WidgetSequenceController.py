from app.Domain.WidgetSequence.Services.WidgetSequenceService import WidgetSequenceService
from app.Http.Requests.Backoffice.WidgetSequenceController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.WidgetSequenceController.WidgetSequenceCollectionResource import WidgetSequenceCollectionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from rest_framework import status, viewsets


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
        return WidgetSequenceCollectionResource({"data": widgetSequence})
