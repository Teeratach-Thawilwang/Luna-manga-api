from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.Domain.Authentication.Services.OAuthAccessTokenService import OAuthAccessTokenService
from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Exceptions.InActiveAccountException import InActiveAccountException
from app.Http.Requests.Store.SessionController.RefreshTokenRequest import RefreshTokenRequest
from app.Http.Requests.Store.SessionController.SessionRequest import SessionRequest
from app.Http.Requests.Store.SessionController.TokenRequest import TokenRequest
from app.Http.Resources.Store.SessionController.TokenResource import TokenResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Notifications.CustomerRegisterEmailNotification import CustomerRegisterEmailNotification
from app.Services.Helpers import getRequestMeta


class SessionController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    customerService = CustomerService()
    oAuthAccessTokenService = OAuthAccessTokenService()

    def initial(self, request, *args, **kwargs):
        request.authentication = ["revoke"]
        super().initial(request, *args, **kwargs)

    def token(self, request):
        TokenRequest(request)

        params = request.params
        meta = getRequestMeta(request)
        oAuthToken = OAuthAccessTokenService().createGuestToken(params["client_id"], meta)
        return TokenResource(oAuthToken, status=status.HTTP_200_OK)

    def session(self, request):
        SessionRequest(request)

        params = request.params
        meta = getRequestMeta(request)
        customer = self.customerService.getByEmail(params["email"])
        self.customerService.checkPassword(customer, params["password"])

        if not self.customerService.isVerifiedEmail(customer):
            CustomerRegisterEmailNotification(customer)
            raise InActiveAccountException({"message": "Need verify email."})

        if not self.customerService.isActive(customer):
            raise InActiveAccountException({"message": "Inactive Account"})

        if self.customerService.isDelete(customer):
            raise InActiveAccountException({"message": "Account was deleted."})

        oAuthToken = self.oAuthAccessTokenService.createAccountToken(params["client_id"], customer, meta)

        return TokenResource(oAuthToken, status=status.HTTP_200_OK)

    def social_session(self, request):
        # ทำการประมวลผล request ในส่วนของ socialSession
        return Response({"message": "Social session request processed"}, status=status.HTTP_200_OK)

    def refresh(self, request):
        RefreshTokenRequest(request)

        params = request.params
        meta = getRequestMeta(request)
        oAuthToken = self.oAuthAccessTokenService.refreshToken(params["refresh_token"], meta)
        return TokenResource(oAuthToken, status=status.HTTP_200_OK)

    def revoke(self, request):
        auth = request.auth

        self.oAuthAccessTokenService.revokeToken(auth.access_token)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
