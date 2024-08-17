from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from app.Domain.Story.Services.StoryService import StoryService
from app.Enums.StatusEnum import StoryStatusEnum
from app.Http.Requests.Store.CategoryStoryController.IndexRequest import IndexRequest
from app.Http.Resources.Store.CategoryStoryController.CategoryStoryCollectionResource import CategoryStoryCollectionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware


class CategoryStoryController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index"]

        super().initial(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS))
    def index(self, request, id):
        IndexRequest(request)

        params = request.params
        params["category_id"] = id
        params["status__in"] = [StoryStatusEnum.ONGOING, StoryStatusEnum.FINISHED]
        paginated = StoryService().search(params).paginate()
        return CategoryStoryCollectionResource(paginated)
