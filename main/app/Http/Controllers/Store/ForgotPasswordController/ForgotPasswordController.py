from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Http.Requests.Store.ForgotPasswordController.ForgotPasswordRequest import ForgotPasswordRequest
from app.Http.Requests.Store.ForgotPasswordController.ResetPasswordRequest import ResetPasswordRequest
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Notifications.PasswordChangedEmailNotification import PasswordChangedEmailNotification
from app.Notifications.ResetPasswordEmailNotification import ResetPasswordEmailNotification
from app.Services.EmailService import EmailService
from django.http import HttpResponse
from rest_framework import status, viewsets


class ForgotPasswordController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["forgotPassword", "resetPassword"]
        super().initial(request, *args, **kwargs)

    def forgotPassword(self, request):
        ForgotPasswordRequest(request)

        params = request.params
        customer = CustomerService().findBy({"email": params["email"]}).first()

        if customer is None:
            raise ResourceNotFoundException({"message": "Resource Not Found."})

        ResetPasswordEmailNotification(customer)

        return HttpResponse(status=status.HTTP_200_OK)

    def resetPassword(self, request):
        ResetPasswordRequest(request)

        params = request.params
        customer = EmailService().getCustomerFromResetPasswordCode(params["code"])

        if customer is None:
            raise ResourceNotFoundException({"message": "Resource Not Found."})

        CustomerService().resetPassword(customer, params["password"])

        PasswordChangedEmailNotification(customer)

        return HttpResponse(status=status.HTTP_200_OK)
