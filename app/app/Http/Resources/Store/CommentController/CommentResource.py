from django.db.models import Sum
from django.http import JsonResponse

from app.Domain.Comment.Models.Comment import Comment
from app.Domain.Comment.Services.CommentService import CommentService
from app.Domain.Customer.Models.Customer import Customer
from app.Services.LocalTime import localTime


class CommentResource(JsonResponse):
    def __init__(self, comment: Comment, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        commentService = CommentService()
        comment = commentService.findBy({"id": comment.id})
        comment = comment.prefetch_related("customer__fileable__file", "commentreaction_set")
        comment = comment.annotate(like__sum=Sum("commentreaction__like"))
        comment = comment.annotate(dislike__sum=Sum("commentreaction__dislike"))
        comment = comment.first()

        self.data = {
            "id": comment.id,
            "message": comment.text,
            "commenter": commentService.getCommenter(comment),
            "reaction": commentService.transformReactionByCommentAndCustomer(comment, customer),
            "created_at": localTime(comment.created_at),
            "updated_at": localTime(comment.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
