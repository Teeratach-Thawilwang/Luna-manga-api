from sys import modules
from typing import Any

from app.Domain.Comment.Models.Comment import Comment
from app.Domain.Comment.Models.CommentReaction import CommentReaction
from app.Domain.Customer.Models.Customer import Customer
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate
from django.db.models import Q, Sum
from django.db.models.query import QuerySet
from django.utils import timezone

if "FileableService" not in modules:
    from app.Domain.File.Services.FileableService import FileableService


class CommentService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id"]
        self.querySet = Comment.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> Comment:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Comment:
        return self.querySet.create(**params)

    def update(self, id: int, params: dict[str, Any]) -> Comment:
        params["updated_at"] = timezone.now()
        try:
            self.querySet.filter(pk=id).update(**params)
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def updateReaction(self, commentId: int, customerId: int, params: dict[str, Any]) -> Comment:
        params["updated_at"] = timezone.now()
        updateParams = {}

        if "like" in params:
            updateParams["like"] = params["like"]
        if "dislike" in params:
            updateParams["dislike"] = params["dislike"]

        try:
            CommentReaction.objects.update_or_create(customer_id=customerId, comment_id=commentId, defaults=updateParams)
            return self.querySet.get(pk=commentId)
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
            self.orderBy = params["order_by"]

        # For front-side
        if "chapter_id" in params:
            self.query += [Q(chapter_id__exact=params["chapter_id"][0])]

        return self

    def paginate(self) -> list:
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)

    def transformReactionByCommentAndCustomer(self, comment: Comment, customer: Customer | None) -> dict[str]:
        reactionSum: dict[str] = comment.commentreaction_set.aggregate(Sum("like"), Sum("dislike"))
        like = reactionSum["like__sum"]
        like = 0 if like == None else like

        dislike = reactionSum["dislike__sum"]
        dislike = 0 if dislike == None else dislike

        if customer == None:
            isLiked = False
            isDisliked = False
        else:
            commentReaction = comment.commentreaction_set.filter(customer_id=customer.id).first()
            if commentReaction == None:
                isLiked = False
                isDisliked = False
            else:
                isLiked = True if commentReaction.like > 0 else False
                isDisliked = True if commentReaction.dislike > 0 else False

        return {
            "like": like,
            "dislike": dislike,
            "is_liked": isLiked,
            "is_disliked": isDisliked,
        }

    def getCommenter(self, comment: Comment) -> dict[str]:
        customer: Customer = comment.customer

        displayName = customer.nick_name
        if displayName == None or len(displayName) == 0:
            displayName = f"{customer.first_name} {customer.last_name}"

        return {
            "id": customer.id,
            "display_name": displayName,
            "images": FileableService().transformImagesByCollection(customer.fileable, CollectionNameEnum.PROFILE_IMAGE, "store"),
        }
