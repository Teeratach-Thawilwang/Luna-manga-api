from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Post.Services.PostService import PostService
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.PostController.IndexRequest import IndexRequest
from app.Http.Requests.Store.PostController.StoreRequest import StoreRequest
from app.Http.Requests.Store.PostController.UpdateRequest import UpdateRequest
from app.Http.Resources.Store.PostController.PostCollectionResource import PostCollectionResource
from app.Http.Resources.Store.PostController.PostResource import PostResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class PostController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "store", "update", "destroy"]
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        customer: Customer = request.user
        posts = PostService().search(params).paginate()
        return PostCollectionResource(posts, customer, status=status.HTTP_200_OK)

    def store(self, request):
        StoreRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        reqParams = request.params
        params = {"customer_id": customer.id, "text": reqParams["message"]}
        post = PostService().create(params)

        return PostResource(post, customer, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        post = PostService().getById(id)
        if post.customer.id != customer.id:
            raise PermissionException({"message": "You have no permission."})

        reqParams = request.params
        params = {"customer_id": customer.id, "text": reqParams["message"]}
        post = PostService().update(post.id, params)

        return PostResource(post, customer, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        post = PostService().getById(id)
        if post.customer.id != customer.id:
            raise PermissionException({"message": "You have no permission."})

        PostService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
