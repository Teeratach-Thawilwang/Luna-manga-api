from app.Domain.Category.Services.CategoryService import CategoryService
from app.Enums.StatusEnum import CategoryStatusEnum
from app.Http.Requests.Store.CategoryController.IndexRequest import IndexRequest
from app.Http.Resources.Store.CategoryController.CategoryCollectionResource import CategoryCollectionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets


class CategoryController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index"]
        super().initial(request, *args, **kwargs)

    # @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS))
    def index(self, request):
        IndexRequest(request)

        params = request.params
        params["status"] = [CategoryStatusEnum.ACTIVE]

        if params["per_page"][0] == "all":
            params["per_page"][0] = 100

        paginated = CategoryService().search(params).paginate()
        return CategoryCollectionResource(paginated)
