from django.http import HttpResponse
from rest_framework import status, viewsets

from app.Domain.Authentication.Services.OAuthAccessTokenService import OAuthAccessTokenService
from app.Domain.User.Services.UserService import UserService
from app.Http.Requests.Backoffice.SessionController.RefreshTokenRequest import RefreshTokenRequest
from app.Http.Requests.Backoffice.SessionController.SessionRequest import SessionRequest
from app.Http.Requests.Backoffice.SessionController.TokenRequest import TokenRequest
from app.Http.Resources.Backoffice.SessionController.TokenResource import TokenResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Services.Helpers import getRequestMeta


class SessionController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["revoke"]
        super().initial(request, *args, **kwargs)

    # Unused
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
        user = UserService().getByEmail(params["email"])
        UserService().checkPassword(user, params["password"])
        UserService().checkActiveUser(user)

        oAuthToken = OAuthAccessTokenService().createAccountToken(params["client_id"], user, meta)

        return TokenResource(oAuthToken, status=status.HTTP_200_OK)

    def refresh(self, request):
        RefreshTokenRequest(request)

        params = request.params
        meta = getRequestMeta(request)
        oAuthToken = OAuthAccessTokenService().refreshToken(params["refresh_token"], meta)
        return TokenResource(oAuthToken, status=status.HTTP_200_OK)

    def revoke(self, request):
        auth = request.auth

        OAuthAccessTokenService().revokeToken(auth.access_token)
        return HttpResponse(status=status.HTTP_200_OK)
