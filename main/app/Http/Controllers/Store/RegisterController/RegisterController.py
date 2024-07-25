from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Exceptions.ConfirmEmailInvalidException import ConfirmEmailInvalidException
from app.Http.Requests.Store.RegisterController.ConfirmEmailRequest import ConfirmEmailRequest
from app.Http.Requests.Store.RegisterController.RegisterRequest import RegisterRequest
from app.Http.Resources.Store.RegisterController.CustomerResource import CustomerResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Notifications.CustomerRegisterEmailNotification import CustomerRegisterEmailNotification
from app.Services.EmailService import EmailService
from django.http import HttpResponse
from rest_framework import status, viewsets


class RegisterController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["register", "confirmEmail"]
        super().initial(request, *args, **kwargs)

    def register(self, request):
        RegisterRequest(request)

        params = request.params
        params["customer_group_id"] = 1  # Default group member.
        customer = CustomerService().create(params)

        CustomerRegisterEmailNotification(customer)

        return CustomerResource(customer, status=status.HTTP_201_CREATED)

    def confirmEmail(self, request):
        ConfirmEmailRequest(request)

        params = request.params
        customer = EmailService().getVerifiedCustomerFromCode(params["code"])

        if customer is None:
            raise ConfirmEmailInvalidException({"message": "Resource Not Found."})

        if customer.email_verified_at is not None:
            raise ConfirmEmailInvalidException({"message": "Email is verified already."})

        CustomerService().emailVerified(customer)
        return HttpResponse(status=status.HTTP_200_OK)
