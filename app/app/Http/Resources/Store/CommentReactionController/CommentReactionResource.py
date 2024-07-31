from app.Domain.Comment.Models.Comment import Comment
from app.Domain.Comment.Services.CommentService import CommentService
from app.Domain.Customer.Models.Customer import Customer
from django.http import JsonResponse


class CommentReactionResource(JsonResponse):
    def __init__(self, post: Comment, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = CommentService().transformReactionByCommentAndCustomer(post, customer)
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
