from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Post.Services.PostService import PostService
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.PostReactionController.UpdateRequest import UpdateRequest
from app.Http.Resources.Store.PostReactionController.PostReactionResource import PostReactionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from rest_framework import status, viewsets


class PostReactionController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["update"]
        super().initial(request, *args, **kwargs)

    def update(self, request, id):
        UpdateRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        params = request.params
        post = PostService().updateReaction(id, customer.id, params)

        return PostReactionResource(post, customer, status=status.HTTP_200_OK)
