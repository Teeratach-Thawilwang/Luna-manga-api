import json
from sys import modules
from typing import Any

from django.db.models import Q, Sum
from django.db.models.query import QuerySet
from django.utils import timezone

from app.Domain.Banner.Models.Banner import Banner
from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Chapter.Models.ChapterReaction import ChapterReaction
from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Story.Models.Story import Story
from app.Domain.User.Models.User import User
from app.Enums.BannerTypeEnum import BannerTypeEnum
from app.Enums.CategoryEnum import CategoryEnum
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Enums.EventEnum import EventEnum
from app.Enums.OrderByEnum import OrderByEnum
from app.Enums.StatusEnum import BannerStatusEnum, ChapterStatusEnum
from app.Event.Event import Event
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Helpers import getCache, getSecondsUntilTomorrow, setCache
from app.Services.Paginator import paginate

if "FileableService" not in modules:
    from app.Domain.File.Services.FileableService import FileableService

if "BannerService" not in modules:
    from app.Domain.Banner.Services.BannerService import BannerService


class ChapterService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id", "name"]
        self.querySet = Chapter.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> Chapter:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Chapter:
        imageId = None

        if "cover_image_id" in params:
            imageId = params["cover_image_id"]
            del params["cover_image_id"]

        chapter = self.querySet.create(**params)

        if imageId != None:
            FileableService().syncSingleFileable(chapter.id, "chapter", imageId, CollectionNameEnum.CHAPTER_COVER_IMAGE)
        return chapter

    def update(self, id: int, params: dict[str, Any]) -> Chapter:
        imageId = None
        params["updated_at"] = timezone.now()

        if "cover_image_id" in params:
            imageId = params["cover_image_id"]
            del params["cover_image_id"]

        try:
            self.querySet.filter(pk=id).update(**params)

            if imageId != None:
                FileableService().syncSingleFileable(id, "chapter", imageId, CollectionNameEnum.CHAPTER_COVER_IMAGE)

            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def updateReaction(self, chapterId: int, customerId: int, params: dict[str, Any]) -> Chapter:
        params["updated_at"] = timezone.now()
        updateParams = {}

        if "like" in params:
            updateParams["like"] = params["like"]
        if "dislike" in params:
            updateParams["dislike"] = params["dislike"]

        try:
            ChapterReaction.objects.update_or_create(customer_id=customerId, chapter_id=chapterId, defaults=updateParams)
            return self.querySet.get(pk=chapterId)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def getFileIdsFromChapterText(self, text: str) -> list[int]:
        nodes = json.loads(text)
        fileIds = []
        for node in nodes:
            if "file_id" in node:
                fileIds.append(node["file_id"])
        return fileIds

    def createFileableForChapter(self, chapterId: int, chapterText: str):
        fileIds = self.getFileIdsFromChapterText(chapterText)
        FileableService().syncFileableByFileIds(chapterId, "chapter", fileIds)

    def deleteById(self, id: int) -> None:
        try:
            model = self.querySet.get(pk=id)
            model.delete()
            self.deleteBannerByChapterId(id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteBannerByChapterId(self, id: int):
        params = {
            "model_id": id,
            "type": BannerTypeEnum.CHAPTER,
        }
        banner: Banner | None = BannerService().findBy(params).first()
        if banner != None:
            banner.delete()

    def prefetch(self, *relations: tuple):
        self.querySet = self.querySet.prefetch_related(*relations)
        return self

    def search(self, params: dict[str, Any]):
        if "q" in params:
            q: str = params["q"][0]
            if q.isnumeric():
                self.query += [Q(id__exact=q)]
            else:
                self.query += [Q(name__istartswith=q)]

        if "status" in params:
            self.query += [Q(status=params["status"])]

        if "type" in params:
            self.query += [Q(type__exact=params["type"][0])]

        if "start_date" in params:
            self.query += [Q(created_at__gte=params["start_date"][0])]

        if "end_date" in params:
            self.query += [Q(created_at__lte=params["end_date"][0])]

        if "is_delete" in params:
            self.query += [Q(is_delete=params["is_delete"])]

        if "page" in params:
            self.page = int(params["page"][0])

        if "per_page" in params:
            self.perPage = int(params["per_page"][0])

        if "order_by" in params:
            orderBy = params["order_by"]
            self.orderBy = orderBy

            if orderBy[0] == OrderByEnum.ASC:
                self.orderBy = ["id"]
            if orderBy[0] == OrderByEnum.DESC:
                self.orderBy = ["-id"]

        # For front-side
        if "slug" in params:
            self.query += [Q(story__slug=params["slug"][0])]

        return self

    def paginate(self) -> list:
        self.prefetch("fileable__file")
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)

    def getScore(self, chapter: Chapter) -> int:
        totalReaction = chapter.chapterreaction_set.count()
        if totalReaction == 0:
            return 0

        like = chapter.chapterreaction_set.aggregate(Sum("like"))["like__sum"]
        like = 0 if like == None else like
        return float("{:.2f}".format(like / totalReaction))

    def transformReactionByChapterAndCustomer(self, chapter: Chapter, customer: Customer | None) -> dict[str]:
        reactionSum: dict[str] = chapter.chapterreaction_set.aggregate(Sum("like"), Sum("dislike"))
        like = reactionSum["like__sum"]
        like = 0 if like == None else like

        dislike = reactionSum["dislike__sum"]
        dislike = 0 if dislike == None else dislike

        if customer == None:
            isLiked = False
            isDisliked = False
        else:
            chapterReaction = chapter.chapterreaction_set.filter(customer_id=customer.id).first()
            if chapterReaction == None:
                isLiked = False
                isDisliked = False
            else:
                isLiked = True if chapterReaction.like > 0 else False
                isDisliked = True if chapterReaction.dislike > 0 else False

        return {
            "like": like,
            "dislike": dislike,
            "is_liked": isLiked,
            "is_disliked": isDisliked,
        }

    def getChapteListByStory(self, story: Story) -> list:
        chapters = story.chapter_set.order_by("-chapter_number")
        data = []
        for chapter in chapters:
            data.append(
                {
                    "id": chapter.id,
                    "name": chapter.name,
                    "chapter_number": chapter.chapter_number,
                }
            )

        return data

    def setViewCountCacheByChapter(self, chapter: Chapter) -> None:
        match chapter.type:
            case CategoryEnum.MANGA:
                currentCount = getCache("manga_view_count", 0)
                setCache("manga_view_count", currentCount + 1, getSecondsUntilTomorrow())
            case CategoryEnum.NOVEL:
                currentCount = getCache("novel_view_count", 0)
                setCache("novel_view_count", currentCount + 1, getSecondsUntilTomorrow())

    def mapChapterStatusToBannerStatus(self, status: ChapterStatusEnum) -> BannerStatusEnum:
        match status:
            case ChapterStatusEnum.ACTIVE:
                return BannerStatusEnum.ACTIVE
            case ChapterStatusEnum.INACTIVE:
                return BannerStatusEnum.INACTIVE

    def updateOrCreateBannerFromChapter(self, chapter: Chapter, user: User) -> None:
        bannerStatus = self.mapChapterStatusToBannerStatus(chapter.status)
        bannerParams = {
            "name": chapter.name,
            "title": chapter.story.name,
            "type": BannerTypeEnum.CHAPTER,
            "link": f"/story/{chapter.story.slug}/{chapter.chapter_number}",
            "status": bannerStatus,
            "model_id": chapter.id,
            "updated_by": user,
        }

        queryParams = {
            "model_id": chapter.id,
            "type": BannerTypeEnum.CHAPTER,
        }
        banner: Banner | None = BannerService().findBy(queryParams).first()
        if banner == None:
            banner = BannerService().create(bannerParams)
        else:
            banner = BannerService().update(banner.id, bannerParams)

        syncParams = {
            "banner": banner,
            "storyId": None,
            "chapterId": chapter.id,
            "imageIds": [],
        }
        Event(EventEnum.SYNC_BANNER_FILEABLE, syncParams)
