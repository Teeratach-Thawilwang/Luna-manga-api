from django.db.models import Sum
from django.http import JsonResponse

from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Post.Services.PostService import PostService
from app.Services.LocalTime import localTime


class PostCollectionResource(JsonResponse):
    def __init__(self, data, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(customer), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self, customer: Customer | None):
        data = []
        postService = PostService()
        posts = self.data["data"].prefetch_related("customer__fileable__file", "postreaction_set")
        posts = posts.annotate(like__sum=Sum("postreaction__like"))
        posts = posts.annotate(dislike__sum=Sum("postreaction__dislike"))

        for post in posts:
            data.append(
                {
                    "id": post.id,
                    "message": post.text,
                    "commenter": postService.getCommenter(post),
                    "reaction": postService.transformReactionByPostAndCustomer(post, customer),
                    "created_at": localTime(post.created_at),
                    "updated_at": localTime(post.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
