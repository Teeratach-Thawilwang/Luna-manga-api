from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets

from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Story.Services.StoryService import StoryService
from app.Enums.CachePagePrefixEnum import CachePagePrefixEnum
from app.Enums.StatusEnum import StoryStatusEnum
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Http.Requests.Store.StoryController.StorySearchRequest import StorySearchRequest
from app.Http.Resources.Store.StoryController.StoryResource import StoryResource
from app.Http.Resources.Store.StoryController.StorySearchCollectionResource import StorySearchCollectionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware


class StoryController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["storySearch", "show"]
        super().initial(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS, key_prefix=CachePagePrefixEnum.STORE_STORY_SEARCH))
    def storySearch(self, request):
        StorySearchRequest(request)

        params = request.params
        paginated = StoryService().search(params).paginate()
        return StorySearchCollectionResource(paginated)

    @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS, key_prefix=CachePagePrefixEnum.STORE_STORY_SHOW))
    def show(self, request, slug):
        customer: Customer | None = request.user

        params = {
            "slug": slug,
            "status__in": [StoryStatusEnum.ONGOING, StoryStatusEnum.FINISHED],
        }
        story = StoryService().findBy(params).first()
        if story == None:
            raise ResourceNotFoundException({"message": "Story does not exist."})

        return StoryResource(story, customer, status=status.HTTP_200_OK)
