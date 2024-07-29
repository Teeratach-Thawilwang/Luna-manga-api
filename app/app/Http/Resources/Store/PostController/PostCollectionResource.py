from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Post.Services.PostService import PostService
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class PostCollectionResource(JsonResponse):
    def __init__(self, data, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(customer), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self, customer: Customer | None):
        data = []
        postService = PostService()
        for post in self.data["data"]:
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
