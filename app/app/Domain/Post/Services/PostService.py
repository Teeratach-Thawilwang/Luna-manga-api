from sys import modules
from typing import Any

from django.db.models import Q, Sum
from django.db.models.query import QuerySet
from django.utils import timezone

from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Post.Models.Post import Post
from app.Domain.Post.Models.PostReaction import PostReaction
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Enums.OrderByEnum import OrderByEnum
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate

if "FileableService" not in modules:
    from app.Domain.File.Services.FileableService import FileableService


class PostService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id"]
        self.querySet = Post.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> Post:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Post:
        return self.querySet.create(**params)

    def update(self, id: int, params: dict[str, Any]) -> Post:
        params["updated_at"] = timezone.now()
        try:
            self.querySet.filter(pk=id).update(**params)
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def updateReaction(self, postId: int, customerId: int, params: dict[str, Any]) -> Post:
        params["updated_at"] = timezone.now()
        updateParams = {}

        if "like" in params:
            updateParams["like"] = params["like"]
        if "dislike" in params:
            updateParams["dislike"] = params["dislike"]

        try:
            PostReaction.objects.update_or_create(customer_id=customerId, post_id=postId, defaults=updateParams)
            return self.querySet.get(pk=postId)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteById(self, id: int) -> None:
        try:
            model = self.querySet.get(pk=id)
            model.delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

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

        if "start_date" in params:
            self.query += [Q(created_at__gte=params["start_date"][0])]

        if "end_date" in params:
            self.query += [Q(created_at__lte=params["end_date"][0])]

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
        if "customer_id" in params:
            self.query += [Q(customer_id__exact=params["customer_id"][0])]

        return self

    def paginate(self) -> list:
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)

    def transformReactionByPostAndCustomer(self, post: Post, customer: Customer | None) -> dict[str]:
        if hasattr(post, "like__sum") and hasattr(post, "dislike__sum"):
            like = post.like__sum
            dislike = post.dislike__sum
        else:
            reactionSum: dict[str] = post.postreaction_set.aggregate(Sum("like"), Sum("dislike"))
            like = reactionSum["like__sum"]
            dislike = reactionSum["dislike__sum"]

        like = 0 if like == None else like
        dislike = 0 if dislike == None else dislike

        if customer == None:
            isLiked = False
            isDisliked = False
        else:
            postReactions = post.postreaction_set.all()
            postReaction = None
            for reaction in postReactions:
                if reaction.customer_id == customer.id:
                    postReaction = reaction
                    break

            if postReaction == None:
                isLiked = False
                isDisliked = False
            else:
                isLiked = True if postReaction.like > 0 else False
                isDisliked = True if postReaction.dislike > 0 else False

        return {
            "like": like,
            "dislike": dislike,
            "is_liked": isLiked,
            "is_disliked": isDisliked,
        }

    def getCommenter(self, post: Post) -> dict[str]:
        customer: Customer = post.customer

        displayName = customer.nick_name
        if displayName == None or len(displayName) == 0:
            displayName = f"{customer.first_name} {customer.last_name}"

        return {
            "id": customer.id,
            "display_name": displayName,
            "images": FileableService().transformImagesByCollection(customer.fileable.all(), CollectionNameEnum.PROFILE_IMAGE, "store"),
        }
