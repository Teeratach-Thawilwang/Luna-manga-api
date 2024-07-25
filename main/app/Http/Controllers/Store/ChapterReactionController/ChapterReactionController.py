from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.Customer.Models.Customer import Customer
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.ChapterReactionController.UpdateRequest import UpdateRequest
from app.Http.Resources.Store.ChapterReactionController.ChapterReactionResource import ChapterReactionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from rest_framework import status, viewsets


class ChapterReactionController(viewsets.ModelViewSet):
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
        chapter = ChapterService().updateReaction(id, customer.id, params)

        return ChapterReactionResource(chapter, customer, status=status.HTTP_200_OK)
