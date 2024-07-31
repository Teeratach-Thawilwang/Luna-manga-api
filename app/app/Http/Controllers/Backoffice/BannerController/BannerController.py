from app.Domain.Banner.Services.BannerService import BannerService
from app.Enums.EventEnum import EventEnum
from app.Event.Event import Event
from app.Http.Requests.Backoffice.BannerController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.BannerController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.BannerController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.BannerController.BannerCollectionResource import BannerCollectionResource
from app.Http.Resources.Backoffice.BannerController.BannerResource import BannerResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class BannerController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "banner.view": ["index", "show"],
            "banner.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = BannerService().search(params).paginate()
        return BannerCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params: dict = request.params
        storyId = params.get("story_id", None)
        chapterId = params.get("chapter_id", None)
        imageIds = params.get("image_ids", [])
        del params["story_id"]
        del params["chapter_id"]
        del params["image_ids"]

        if storyId != None:
            params["model_id"] = storyId
        if chapterId != None:
            params["model_id"] = chapterId

        params["updated_by"] = request.user
        service = BannerService().prefetch("fileable__file")
        banner = service.create(params)

        syncParams = {
            "banner": banner,
            "storyId": storyId,
            "chapterId": chapterId,
            "imageIds": imageIds,
        }
        Event(EventEnum.SYNC_BANNER_FILEABLE, syncParams)

        return BannerResource(banner, status=status.HTTP_201_CREATED)

    def show(self, request, id):
        service = BannerService().prefetch("fileable__file")
        banner = service.getById(id)
        return BannerResource(banner, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params: dict = request.params
        storyId = params.get("story_id", None)
        chapterId = params.get("chapter_id", None)
        imageIds = params.get("image_ids", [])
        del params["story_id"]
        del params["chapter_id"]
        del params["image_ids"]

        if storyId != None:
            params["model_id"] = storyId
        if chapterId != None:
            params["model_id"] = chapterId

        params["updated_by"] = request.user
        service = BannerService().prefetch("fileable__file")
        banner = service.update(id, params)

        syncParams = {
            "banner": banner,
            "storyId": storyId,
            "chapterId": chapterId,
            "imageIds": imageIds,
        }
        Event(EventEnum.SYNC_BANNER_FILEABLE, syncParams)

        return BannerResource(banner, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        BannerService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
