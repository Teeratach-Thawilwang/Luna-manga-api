from app.Domain.User.Models.User import User
from app.Domain.User.Services.UserService import UserService
from app.Exceptions.AuthenticationFailedException import AuthenticationFailedException
from app.Http.Requests.Backoffice.UserController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.UserProfileController.UserProfileResource import UserProfileResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from rest_framework import status, viewsets


class UserProfileController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["show", "update"]

        super().initial(request, *args, **kwargs)

    def show(self, request):
        user = request.user
        isActive = UserService().isActive(user)
        if not isActive:
            raise AuthenticationFailedException({"message": "User inactive."})
        return UserProfileResource(user, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        user: User = request.user
        if user.id != id:
            raise AuthenticationFailedException({"message": "User id invalid."})

        isActive = UserService().isActive(user)
        if not isActive:
            raise AuthenticationFailedException({"message": "User inactive."})

        user = UserService().update(id, params)
        return UserProfileResource(user, status=status.HTTP_200_OK)
