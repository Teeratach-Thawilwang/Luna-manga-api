from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Exceptions.TokenInvalidException import TokenInvalidException
from app.Http.Requests.Store.CustomerProfileController.UpdateRequest import UpdateRequest
from app.Http.Resources.Store.CustomerProfileController.CustomerProfileResource import CustomerProfileResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from rest_framework import status, viewsets


class CustomerProfileController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["show", "update"]
        super().initial(request, *args, **kwargs)

    def show(self, request):
        customer: Customer = request.user
        if customer == None:
            raise TokenInvalidException({"message": "Guest token has no profile."})
        return CustomerProfileResource(customer, status=status.HTTP_200_OK)

    def update(self, request):
        UpdateRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise TokenInvalidException({"message": "Guest token has no profile."})

        params = request.params
        del params["id"]
        customer = CustomerService().update(customer.id, params)

        return CustomerProfileResource(customer, status=status.HTTP_200_OK)
