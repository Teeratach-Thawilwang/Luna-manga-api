from app.Domain.Authentication.Services.OAuthAccessTokenService import OAuthAccessTokenService
from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Exceptions.InActiveAccountException import InActiveAccountException
from app.Http.Requests.Store.SessionController.RefreshTokenRequest import RefreshTokenRequest
from app.Http.Requests.Store.SessionController.SessionRequest import SessionRequest
from app.Http.Requests.Store.SessionController.TokenRequest import TokenRequest
from app.Http.Resources.Store.SessionController.TokenResource import TokenResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Notifications.CustomerRegisterEmailNotification import CustomerRegisterEmailNotification
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response


class SessionController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["revoke"]
        super().initial(request, *args, **kwargs)

    def token(self, request):
        TokenRequest(request)

        params = request.params
        oAuthToken = OAuthAccessTokenService().createGuestToken(params["client_id"])
        return TokenResource(oAuthToken, status=status.HTTP_200_OK)

    def session(self, request):
        SessionRequest(request)

        params = request.params
        customer = CustomerService().getByEmail(params["email"])
        CustomerService().checkPassword(customer, params["password"])

        if not CustomerService().isVerifiedEmail(customer):
            CustomerRegisterEmailNotification(customer)
            raise InActiveAccountException({"message": "Need verify email."})

        if not CustomerService().isActive(customer):
            raise InActiveAccountException({"message": "Inactive Account"})

        if CustomerService().isDelete(customer):
            raise InActiveAccountException({"message": "Account was deleted."})

        oAuthToken = OAuthAccessTokenService().createAccountToken(params["client_id"], customer)

        return TokenResource(oAuthToken, status=status.HTTP_200_OK)

    def social_session(self, request):
        # ทำการประมวลผล request ในส่วนของ socialSession
        return Response({"message": "Social session request processed"}, status=status.HTTP_200_OK)

    def refresh(self, request):
        RefreshTokenRequest(request)

        params = request.params
        oAuthToken = OAuthAccessTokenService().refreshToken(params["refresh_token"])
        return TokenResource(oAuthToken, status=status.HTTP_200_OK)

    def revoke(self, request):
        auth = request.auth

        OAuthAccessTokenService().revokeToken(auth.access_token)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
