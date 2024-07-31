from app.Domain.Widget.Services.WidgetService import WidgetService
from app.Enums.StatusEnum import WidgetStatusEnum
from app.Http.Requests.Store.WidgetController.IndexRequest import IndexRequest
from app.Http.Requests.Store.WidgetController.WidgetBannersRequest import WidgetBannersRequest
from app.Http.Resources.Store.WidgetController.WidgetBannersResource import WidgetBannersResource
from app.Http.Resources.Store.WidgetController.WidgetCollectionResource import WidgetCollectionResource
from app.Http.Resources.Store.WidgetController.WidgetOnPageResource import WidgetOnPageResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets


class WidgetController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "widgetOnPage", "widgetBanners"]
        super().initial(request, *args, **kwargs)

    # @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS))
    def index(self, request):
        IndexRequest(request)

        params = request.params
        params["in_widget_sequence"] = True
        params["status"] = [WidgetStatusEnum.ACTIVE]
        params["order_by"] = ["widgetsequence__sequence"]
        widgets = WidgetService().search(params).paginate()
        return WidgetCollectionResource(widgets, status=status.HTTP_200_OK)

    # @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS))
    def widgetOnPage(self, request):
        widgets = WidgetService().getWidgetOnPage()
        return WidgetOnPageResource(widgets, status=status.HTTP_200_OK)

    # @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS))
    def widgetBanners(self, request, id):
        WidgetBannersRequest(request)

        params = request.params
        page = int(params["page"][0])
        perPage = int(params["per_page"][0])
        widget = WidgetService().getById(id)
        return WidgetBannersResource(widget, page, perPage, status=status.HTTP_200_OK)
