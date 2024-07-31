from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Http.Requests.Backoffice.ChapterController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.ChapterController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.ChapterController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.ChapterController.ChapterCollectionResource import ChapterCollectionResource
from app.Http.Resources.Backoffice.ChapterController.ChapterResource import ChapterResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class ChapterController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "chapter.view": ["index", "show"],
            "chapter.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = ChapterService().search(params).paginate()
        return ChapterCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params = request.params
        service = ChapterService().prefetch("story", "fileable__file")
        chapter = service.create(params)
        service.createFileableForChapter(chapter.id, chapter.text)
        service.updateOrCreateBannerFromChapter(chapter, request.user)

        return ChapterResource(chapter, status=status.HTTP_201_CREATED)

    def show(self, request, id):
        service = ChapterService().prefetch("story", "fileable__file")
        chapter = service.getById(id)
        return ChapterResource(chapter, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        service = ChapterService().prefetch("story", "fileable__file")
        chapter = service.update(id, params)
        service.createFileableForChapter(chapter.id, chapter.text)
        service.updateOrCreateBannerFromChapter(chapter, request.user)

        return ChapterResource(chapter, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        ChapterService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
