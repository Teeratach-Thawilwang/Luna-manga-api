from app.Domain.Widget.Services.WidgetService import WidgetService
from app.Http.Requests.Backoffice.WidgetController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.WidgetController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.WidgetController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.WidgetController.WidgetCollectionResource import WidgetCollectionResource
from app.Http.Resources.Backoffice.WidgetController.WidgetResource import WidgetResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class WidgetController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "widget.view": ["index", "show"],
            "widget.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        service = WidgetService().prefetch("widgetbanner_set")
        paginated = service.search(params).paginate()
        return WidgetCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params = request.params
        service = WidgetService().prefetch("widgetbanner_set")
        widget = service.create(params)

        return WidgetResource(widget, status=status.HTTP_201_CREATED)

    def show(self, request, id):

        service = WidgetService().prefetch("widgetbanner_set")
        widget = service.getById(id)
        return WidgetResource(widget, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        service = WidgetService().prefetch("widgetbanner_set")
        widget = service.update(id, params)

        return WidgetResource(widget, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        WidgetService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
