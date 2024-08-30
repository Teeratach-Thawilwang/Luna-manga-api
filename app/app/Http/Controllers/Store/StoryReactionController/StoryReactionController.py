from rest_framework import status, viewsets

from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Story.Services.StoryService import StoryService
from app.Enums.CachePagePrefixEnum import CachePagePrefixEnum
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.StoryReactionController.UpdateRequest import UpdateRequest
from app.Http.Resources.Store.StoryReactionController.StoryReactionResource import StoryReactionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Services.Helpers import clearAllRedisCacheByKeyPrefix


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
        clearAllRedisCacheByKeyPrefix(CachePagePrefixEnum.STORE_STORY_SHOW)

        return StoryReactionResource(story, customer, status=status.HTTP_200_OK)
