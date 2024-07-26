from sys import modules
from typing import Any

from app.Domain.Banner.Models.Banner import Banner
from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.File.Models.File import File
from app.Domain.Story.Models.Story import Story
from app.Enums.BannerTypeEnum import BannerTypeEnum
from app.Enums.CollectionEnum import CollectionEnum, CollectionNameEnum
from app.Enums.EventEnum import EventEnum
from app.Enums.StatusEnum import BannerStatusEnum
from app.Event.Event import Event
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone

if "FileableService" not in modules:
    from app.Domain.File.Services.FileableService import FileableService
if "FileService" not in modules:
    from app.Domain.File.Services.FileService import FileService


class BannerService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id", "name"]
        self.querySet = Banner.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id) -> Banner:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Banner:
        return self.querySet.create(**params)

    def update(self, id: int, params: dict[str, Any]) -> Banner:
        params["updated_at"] = timezone.now()

        try:
            self.querySet.filter(pk=id).update(**params)
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteById(self, id) -> None:
        try:
            banner = self.querySet.get(pk=id)
            banner.delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def prefetch(self, *relations: tuple):
        self.querySet = self.querySet.prefetch_related(*relations)
        return self

    def search(self, params):
        if "q" in params:
            q: str = params["q"][0]
            if q.isnumeric():
                self.query += [Q(id__exact=q)]
            else:
                self.query += [Q(email__startswith=q) | Q(first_name__startswith=q)]

        if "status" in params:
            self.query += [Q(status__exact=params["status"][0])]

        if "type" in params:
            self.query += [Q(type__exact=params["type"][0])]

        if "start_date" in params:
            self.query += [Q(created_at__gte=params["start_date"][0])]

        if "end_date" in params:
            self.query += [Q(created_at__lte=params["end_date"][0])]

        if "page" in params:
            self.page = int(params["page"][0])

        if "per_page" in params:
            self.perPage = int(params["per_page"][0])

        if "order_by" in params:
            self.orderBy = params["order_by"]

        return self

    def paginate(self) -> list:
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)

    def isActive(self, banner: Banner):
        return banner.status == BannerStatusEnum.ACTIVE

    def syncBannerFileable(self, bannerId: int, bannerType: BannerTypeEnum, storyId: int | None, chapterId: int | None, imageIds: list[int]) -> None:
        if bannerType == BannerTypeEnum.CHAPTER:
            chapter = Chapter.objects.get(pk=chapterId)
            fileable = chapter.fileable.filter(file__collection_name=CollectionNameEnum.CHAPTER_COVER_IMAGE)
            chapterFile: File = fileable[0].file
            # self.updateOrCreateBannerFileable(bannerId, chapterFile, CollectionNameEnum.BANNER_CHAPTER)
            FileableService().syncSingleFileable(bannerId, "banner", chapterFile.id, chapterFile.collection_name)

        if bannerType == BannerTypeEnum.STORY:
            story = Story.objects.get(pk=storyId)
            fileable = story.fileable.filter(file__collection_name=CollectionNameEnum.STORY_IMAGE)
            storyFile: File = fileable[0].file
            # self.updateOrCreateBannerFileable(bannerId, storyFile, CollectionNameEnum.BANNER_STORY)
            FileableService().syncSingleFileable(bannerId, "banner", storyFile.id, storyFile.collection_name)

        if bannerType in BannerTypeEnum.advertisement():
            files = File.objects.filter(id__in=imageIds)
            for file in files:
                FileableService().syncSingleFileable(bannerId, "banner", file.id, file.collection_name)

    def updateOrCreateBannerFileable(self, bannerId: int, file: File, collectionName: CollectionNameEnum):
        searchParams = {"file_name": file.file_name, "collection_name": collectionName}
        fileSet = FileService().findBy(searchParams).exclude(pk=file.id).order_by("id")
        if fileSet.exists():
            bannerFile: File = fileSet.first()
            FileableService().syncSingleFileable(bannerId, "banner", bannerFile.id, collectionName)
        else:
            uploadFile = FileService().createUploadFileFromFile(file)
            collection = CollectionEnum().get(collectionName)
            bannerFile: File = FileService().create(uploadFile, collection)
            FileableService().syncSingleFileable(bannerId, "banner", bannerFile.id, collectionName)

            extension = "." + uploadFile.name.split(".")[-1]
            uploadFile.name = bannerFile.uuid + extension
            uploadParams = {
                "file": bannerFile,
                "uploadFile": uploadFile,
                "collection": collection,
            }
            Event(EventEnum.UPLOAD_FILE, uploadParams)

    def transformBannerImages(self, banner: Banner, sideUrl: str):
        fileableService = FileableService()
        match banner.type:
            case BannerTypeEnum.CHAPTER:
                return fileableService.transformImagesByCollection(banner.fileable, CollectionNameEnum.CHAPTER_COVER_IMAGE, sideUrl)
            case BannerTypeEnum.STORY:
                return fileableService.transformImagesByCollection(banner.fileable, CollectionNameEnum.STORY_IMAGE, sideUrl)
            case BannerTypeEnum.STORY_WINDOW:
                images = fileableService.transformImagesByCollection(banner.fileable, CollectionNameEnum.BANNER_STORY_WINDOW_1, sideUrl)
                images += fileableService.transformImagesByCollection(banner.fileable, CollectionNameEnum.BANNER_STORY_WINDOW_2, sideUrl)
                images += fileableService.transformImagesByCollection(banner.fileable, CollectionNameEnum.BANNER_STORY_WINDOW_3, sideUrl)
                return images
            case BannerTypeEnum.ADVERTISEMENT_SMALL:
                return fileableService.transformImagesByCollection(banner.fileable, CollectionNameEnum.BANNER_ADVERTISEMENT_SMALL, sideUrl)
            case BannerTypeEnum.ADVERTISEMENT_MEDIUM:
                return fileableService.transformImagesByCollection(banner.fileable, CollectionNameEnum.BANNER_ADVERTISEMENT_MEDIUM, sideUrl)
            case BannerTypeEnum.ADVERTISEMENT_GROUP:
                return fileableService.transformImagesByCollection(banner.fileable, CollectionNameEnum.BANNER_ADVERTISEMENT_GROUP, sideUrl)
