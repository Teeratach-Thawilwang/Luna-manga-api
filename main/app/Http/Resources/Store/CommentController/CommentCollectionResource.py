from app.Domain.Comment.Services.CommentService import CommentService
from app.Domain.Customer.Models.Customer import Customer
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class CommentCollectionResource(JsonResponse):
    def __init__(self, data, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(customer), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self, customer: Customer | None):
        data = []
        commentService = CommentService()
        for comment in self.data["data"]:
            data.append(
                {
                    "id": comment.id,
                    "message": comment.text,
                    "commenter": commentService.getCommenter(comment),
                    "reaction": commentService.transformReactionByCommentAndCustomer(comment, customer),
                    "created_at": localTime(comment.created_at),
                    "updated_at": localTime(comment.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
