from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.Customer.Models.Customer import Customer
from app.Enums.StatusEnum import ChapterStatusEnum
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Http.Resources.Store.ChapterController.ChapterResource import ChapterResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Services.Helpers import setCache
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import status, viewsets


class ChapterController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["show"]
        super().initial(request, *args, **kwargs)

    # @method_decorator(cache_page(settings.CACHE_PAGE_IN_SECONDS))
    # @method_decorator(vary_on_headers("Authorization"))
    def show(self, request, slug, number):
        customer: Customer | None = request.user
        params = {
            "story__slug": slug,
            "chapter_number": number,
            "status": ChapterStatusEnum.ACTIVE,
        }
        chapter: Chapter = ChapterService().findBy(params).first()
        if chapter == None:
            raise ResourceNotFoundException({"message": "Chapter does not exist."})

        chapter = ChapterService().update(chapter.id, {"view_count": chapter.view_count + 1})
        ChapterService().setViewCountCacheByChapter(chapter)
        return ChapterResource(chapter, customer, status=status.HTTP_200_OK)
