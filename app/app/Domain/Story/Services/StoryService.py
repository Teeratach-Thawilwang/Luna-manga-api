from sys import modules
from typing import Any

from django.db.models import Q, Sum
from django.db.models.query import QuerySet
from django.utils import timezone

from app.Domain.Banner.Models.Banner import Banner
from app.Domain.Category.Models.Category import Category
from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Story.Models.Story import Story
from app.Domain.Story.Models.StoryReaction import StoryReaction
from app.Domain.User.Models.User import User
from app.Enums.BannerTypeEnum import BannerTypeEnum
from app.Enums.CategoryEnum import CategoryEnum
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Enums.EventEnum import EventEnum
from app.Enums.StatusEnum import BannerStatusEnum, StoryStatusEnum
from app.Event.Event import Event
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate

if "FileableService" not in modules:
    from app.Domain.File.Services.FileableService import FileableService

if "BannerService" not in modules:
    from app.Domain.Banner.Services.BannerService import BannerService


class StoryService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id", "name"]
        self.querySet = Story.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> Story:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Story:
        imageId = None
        categoryIds = None

        if "category_ids" in params:
            categoryIds = params["category_ids"]
            del params["category_ids"]

        if "cover_image_id" in params:
            imageId = params["cover_image_id"]
            del params["cover_image_id"]

        story = self.querySet.create(**params)
        categoryIds = self.addDefaultCategoryByType(categoryIds, params["type"])
        categories = Category.objects.filter(id__in=categoryIds)
        self.addCategories(story, categories)

        if imageId != None:
            FileableService().syncSingleFileable(story.id, "story", imageId, CollectionNameEnum.STORY_IMAGE)
        return story

    def update(self, id: int, params: dict[str, Any]) -> Story:
        imageId = None
        categoryIds = None
        params["updated_at"] = timezone.now()

        if "category_ids" in params:
            categoryIds = params["category_ids"]
            del params["category_ids"]

        if "cover_image_id" in params:
            imageId = params["cover_image_id"]
            del params["cover_image_id"]

        try:
            self.querySet.filter(pk=id).update(**params)

            if imageId != None:
                FileableService().syncSingleFileable(id, "story", imageId, CollectionNameEnum.STORY_IMAGE)

            categoryIds = self.addDefaultCategoryByType(categoryIds, params["type"])
            self.syncCategory(id, categoryIds)
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def updateReaction(self, storyId: int, customerId: int, params: dict[str, Any]) -> Story:
        params["updated_at"] = timezone.now()
        updateParams = {}

        if "like" in params:
            updateParams["like"] = params["like"]
        if "dislike" in params:
            updateParams["dislike"] = params["dislike"]

        try:
            StoryReaction.objects.update_or_create(customer_id=customerId, story_id=storyId, defaults=updateParams)
            return self.querySet.get(pk=storyId)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteById(self, id: int) -> None:
        try:
            model = self.querySet.get(pk=id)
            model.delete()
            self.deleteBannerByStoryId(id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteBannerByStoryId(self, id: int):
        params = {
            "model_id": id,
            "type": BannerTypeEnum.STORY,
        }
        banner: Banner | None = BannerService().findBy(params).first()
        if banner != None:
            banner.delete()

    def addDefaultCategoryByType(self, categoryIds: list[int], type: CategoryEnum):
        defaultCategoryId = 1  # manga
        if type == CategoryEnum.NOVEL:
            defaultCategoryId = 2  # novel
        categoryIds.append(defaultCategoryId)
        return list(set(categoryIds))

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

        if "is_customer_exist" in params:
            isCustomerNull = not params["is_customer_exist"]
            self.query += [Q(customer_id__isnull=isCustomerNull)]

        if "page" in params:
            self.page = int(params["page"][0])

        if "per_page" in params:
            self.perPage = int(params["per_page"][0])

        if "order_by" in params:
            self.orderBy = params["order_by"]

        # For front-side
        if "category_id" in params:
            self.query += [Q(categories__id=params["category_id"])]

        if "status__in" in params:
            self.query += [Q(status__in=params["status__in"])]

        return self

    def paginate(self) -> list:
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)

    def addCategories(self, story: Story, categories: list[Category]) -> None:
        for category in categories:
            if story.type == category.type:
                story.categories.add(category)

    def removeCategories(self, story: Story, categories: list[Category]) -> None:
        for category in categories:
            story.categories.remove(category)

    def syncCategory(self, modelId: int, categoryIds: list[int]) -> None:
        deleteCategoryIds = []
        story = self.getById(modelId)
        currentCategoryIds = [category["id"] for category in story.categories.values("id")]

        for categoryId in currentCategoryIds:
            if categoryId not in categoryIds:
                deleteCategoryIds.append(categoryId)

            if categoryId in categoryIds:
                index = categoryIds.index(categoryId)
                categoryIds.pop(index)

        addCategories = Category.objects.filter(id__in=categoryIds)
        deleteCategories = Category.objects.filter(id__in=deleteCategoryIds)
        self.addCategories(story, addCategories)
        self.removeCategories(story, deleteCategories)

    def getAuthorName(self, story: Story) -> str:
        if story.customer == None:
            return ""

        return f"{story.customer.first_name} {story.customer.last_name}"

    def getRating(self, story: Story) -> int:
        totalReaction = story.storyreaction_set.count()
        if totalReaction == 0:
            return 0

        like = story.storyreaction_set.aggregate(Sum("like"))["like__sum"]
        like = 0 if like == None else like
        return float("{:.2f}".format(like / totalReaction))

    def getAuthor(self, customer: Customer) -> dict[str]:
        displayName = customer.nick_name
        if displayName == None or len(displayName) == 0:
            displayName = f"{customer.first_name} {customer.last_name}"

        return {
            "id": customer.id,
            "display_name": displayName,
        }

    def getViewCountFromChapter(self, story: Story) -> int:
        viewCount = story.chapter_set.aggregate(Sum("view_count"))["view_count__sum"]
        viewCount = 0 if viewCount == None else viewCount
        return viewCount

    def transformCategories(self, categories: list[Category]) -> dict[str]:
        data = []
        fileableService = FileableService()
        for category in categories:
            data.append(
                {
                    "id": category.id,
                    "name": category.name,
                    "type": category.type,
                    "images": fileableService.transformImagesByCollection(category.fileable.all(), CollectionNameEnum.CATEGORY_IMAGE, "store"),
                }
            )
        return data

    def isBookmark(self, story: Story, customer: Customer | None) -> bool:
        if customer == None:
            return False
        return story.bookmark_set.filter(customer_id=customer.id).first() != None

    def transformReactionByStoryAndCustomer(self, story: Story, customer: Customer | None) -> dict[str]:
        reactionSum: dict[str] = story.storyreaction_set.aggregate(Sum("like"), Sum("dislike"))
        like = reactionSum["like__sum"]
        like = 0 if like == None else like

        dislike = reactionSum["dislike__sum"]
        dislike = 0 if dislike == None else dislike

        if customer == None:
            isLiked = False
            isDisliked = False
        else:
            storyReaction = story.storyreaction_set.filter(customer_id=customer.id).first()
            if storyReaction == None:
                isLiked = False
                isDisliked = False
            else:
                isLiked = True if storyReaction.like > 0 else False
                isDisliked = True if storyReaction.dislike > 0 else False

        return {
            "like": like,
            "dislike": dislike,
            "is_liked": isLiked,
            "is_disliked": isDisliked,
            "rating_score": self.getRating(story),
        }

    def mapStoryStatusToBannerStatus(self, status: StoryStatusEnum) -> BannerStatusEnum:
        match status:
            case StoryStatusEnum.ONGOING:
                return BannerStatusEnum.ACTIVE
            case StoryStatusEnum.FINISHED:
                return BannerStatusEnum.ACTIVE
            case StoryStatusEnum.INACTIVE:
                return BannerStatusEnum.INACTIVE

    def updateOrCreateBannerFromStory(self, story: Story, user: User) -> None:
        bannerStatus = self.mapStoryStatusToBannerStatus(story.status)
        bannerParams = {
            "name": story.name,
            "title": story.name,
            "type": BannerTypeEnum.STORY,
            "link": f"/story/{story.slug}",
            "status": bannerStatus,
            "model_id": story.id,
            "updated_by": user,
        }

        queryParams = {
            "model_id": story.id,
            "type": BannerTypeEnum.STORY,
        }
        banner: Banner | None = BannerService().findBy(queryParams).first()
        if banner == None:
            banner = BannerService().create(bannerParams)
        else:
            banner = BannerService().update(banner.id, bannerParams)

        syncParams = {
            "banner": banner,
            "storyId": story.id,
            "chapterId": None,
            "imageIds": [],
        }
        Event(EventEnum.SYNC_BANNER_FILEABLE, syncParams)
