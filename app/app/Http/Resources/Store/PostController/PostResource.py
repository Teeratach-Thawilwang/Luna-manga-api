from django.db.models import Sum
from django.http import JsonResponse

from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Post.Models.Post import Post
from app.Domain.Post.Services.PostService import PostService
from app.Services.LocalTime import localTime


class PostResource(JsonResponse):
    def __init__(self, post: Post, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        postService = PostService()
        post = postService.findBy({"id": post.id})
        post = post.prefetch_related("customer__fileable__file", "postreaction_set")
        post = post.annotate(like__sum=Sum("postreaction__like"))
        post = post.annotate(dislike__sum=Sum("postreaction__dislike"))
        post = post.first()

        self.data = {
            "id": post.id,
            "message": post.text,
            "commenter": postService.getCommenter(post),
            "reaction": postService.transformReactionByPostAndCustomer(post, customer),
            "created_at": localTime(post.created_at),
            "updated_at": localTime(post.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
