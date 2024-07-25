from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Exceptions.InActiveAccountException import InActiveAccountException
from app.Http.Resources.Store.ProfileController.ProfileResource import ProfileResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from rest_framework import status, viewsets


class ProfileController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["show"]
        super().initial(request, *args, **kwargs)

    def show(self, request, id):
        customer = CustomerService().getById(id)

        if not CustomerService().isActive(customer):
            raise InActiveAccountException({"message": "Inactive Account"})

        if CustomerService().isDelete(customer):
            raise InActiveAccountException({"message": "Account was deleted."})

        return ProfileResource(customer, status=status.HTTP_200_OK)
