from app.Domain.Comment.Services.CommentService import CommentService
from app.Domain.Customer.Models.Customer import Customer
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.CommentReactionController.UpdateRequest import UpdateRequest
from app.Http.Resources.Store.CommentReactionController.CommentReactionResource import CommentReactionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from rest_framework import status, viewsets


class CommentReactionController(viewsets.ModelViewSet):
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
        comment = CommentService().updateReaction(id, customer.id, params)

        return CommentReactionResource(comment, customer, status=status.HTTP_200_OK)
