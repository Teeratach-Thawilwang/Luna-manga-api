from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Story.Services.StoryService import StoryService
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.StoryReactionController.UpdateRequest import UpdateRequest
from app.Http.Resources.Store.StoryReactionController.StoryReactionResource import StoryReactionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from rest_framework import status, viewsets


class StoryReactionController(viewsets.ModelViewSet):
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
        story = StoryService().updateReaction(id, customer.id, params)

        return StoryReactionResource(story, customer, status=status.HTTP_200_OK)
