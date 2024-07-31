from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Enums.StatusEnum import ChapterStatusEnum
from app.Http.Requests.Store.StoryChapterController.IndexRequest import IndexRequest
from app.Http.Resources.Store.StoryChapterController.StoryChapterCollectionResource import StoryChapterCollectionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets


class StoryChapterController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index"]

        super().initial(request, *args, **kwargs)

    # @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS))
    def index(self, request, slug):
        IndexRequest(request)

        params = request.params
        params["slug"] = [slug]
        params["status"] = ChapterStatusEnum.ACTIVE
        paginated = ChapterService().search(params).paginate()
        return StoryChapterCollectionResource(paginated)
