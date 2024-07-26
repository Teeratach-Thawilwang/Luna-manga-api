from app.Domain.Story.Services.StoryService import StoryService
from app.Http.Requests.Backoffice.StoryController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.StoryController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.StoryController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.StoryController.StoryCollectionResource import StoryCollectionResource
from app.Http.Resources.Backoffice.StoryController.StoryResource import StoryResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class StoryController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "story.view": ["index", "show"],
            "story.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        service = StoryService().prefetch("chapter_set", "categories", "fileable__file")
        paginated = service.search(params).paginate()
        return StoryCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params = request.params
        if "customer_id" not in params:
            params["customer_id"] = 1  # Default customer : Admin
        story = StoryService().create(params)
        StoryService().updateOrCreateBannerFromStory(story, request.user)

        return StoryResource(story, status=status.HTTP_201_CREATED)

    def show(self, request, id):
        service = StoryService().prefetch("categories", "fileable__file")
        story = service.getById(id)
        return StoryResource(story, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        service = StoryService().prefetch("categories", "fileable__file")
        story = service.update(id, params)
        StoryService().updateOrCreateBannerFromStory(story, request.user)

        return StoryResource(story, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        StoryService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
