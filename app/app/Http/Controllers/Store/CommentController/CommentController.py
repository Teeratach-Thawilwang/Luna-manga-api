﻿from django.http import HttpResponse
from rest_framework import status, viewsets

from app.Domain.Comment.Services.CommentService import CommentService
from app.Domain.Customer.Models.Customer import Customer
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.CommentController.IndexRequest import IndexRequest
from app.Http.Requests.Store.CommentController.StoreRequest import StoreRequest
from app.Http.Requests.Store.CommentController.UpdateRequest import UpdateRequest
from app.Http.Resources.Store.CommentController.CommentCollectionResource import CommentCollectionResource
from app.Http.Resources.Store.CommentController.CommentResource import CommentResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware


class CommentController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "store", "update", "destroy"]
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        customer: Customer = request.user
        comments = CommentService().search(params).paginate()
        return CommentCollectionResource(comments, customer, status=status.HTTP_200_OK)

    def store(self, request):
        StoreRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        reqParams = request.params
        params = {
            "customer_id": customer.id,
            "chapter_id": reqParams["chapter_id"],
            "text": reqParams["message"],
        }
        comment = CommentService().create(params)

        return CommentResource(comment, customer, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        commentService = CommentService()
        comment = commentService.getById(id)
        if comment.customer.id != customer.id:
            raise PermissionException({"message": "You have no permission."})

        reqParams = request.params
        params = {
            "customer_id": customer.id,
            "chapter_id": reqParams["chapter_id"],
            "text": reqParams["message"],
        }
        comment = commentService.update(comment.id, params)

        return CommentResource(comment, customer, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        commentService = CommentService()
        comment = commentService.getById(id)
        if comment.customer.id != customer.id:
            raise PermissionException({"message": "You have no permission."})

        commentService.deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
