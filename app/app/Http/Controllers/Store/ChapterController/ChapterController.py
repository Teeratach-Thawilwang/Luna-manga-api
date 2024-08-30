from django.conf import settings
from rest_framework import status, viewsets

from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.Customer.Models.Customer import Customer
from app.Enums.CachePagePrefixEnum import CachePagePrefixEnum
from app.Enums.CategoryEnum import CategoryEnum
from app.Enums.StatusEnum import ChapterStatusEnum
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Http.Resources.Store.ChapterController.ChapterResource import ChapterResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Services.Helpers import getCache, setCache


class ChapterController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["show"]
        super().initial(request, *args, **kwargs)

    def show(self, request, slug, number):
        customer: Customer | None = request.user
        params = {
            "story__slug": slug,
            "chapter_number": number,
            "status": ChapterStatusEnum.ACTIVE,
        }

        chapterService = ChapterService()
        chapter: Chapter = chapterService.findBy(params).first()
        if chapter == None:
            raise ResourceNotFoundException({"message": "Chapter does not exist."})

        chapter = chapterService.update(chapter.id, {"view_count": chapter.view_count + 1})
        chapterService.setViewCountCacheByChapter(chapter)

        keyPrefix = CachePagePrefixEnum.STORE_CHAPTER_SHOW
        key = f"{keyPrefix}slug:{slug}_chapter_number:{number}"
        response = getCache(key, None)
        if response != None:
            return response

        if chapter.type == CategoryEnum.NOVEL:
            chapter.text = chapterService.loadChapterTextFromStorage(chapter)

        response = ChapterResource(chapter, customer, status=status.HTTP_200_OK)
        setCache(key, response, settings.CACHE_PAGE_IN_SECONDS)
        return response
