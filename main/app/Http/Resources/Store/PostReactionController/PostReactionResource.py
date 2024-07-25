from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Post.Models.Post import Post
from app.Domain.Post.Services.PostService import PostService
from django.http import JsonResponse


class PostReactionResource(JsonResponse):
    def __init__(self, post: Post, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = PostService().transformReactionByPostAndCustomer(post, customer)
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
