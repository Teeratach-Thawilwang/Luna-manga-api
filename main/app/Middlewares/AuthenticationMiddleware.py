from app.Domain.Authentication.Services.OAuthAccessTokenService import OAuthAccessTokenService
from app.Exceptions.AuthenticationFailedException import AuthenticationFailedException
from rest_framework.authentication import BaseAuthentication


class AuthenticationMiddleware(BaseAuthentication):
    def authenticate(self, request):
        requestMethod = str(request.method).lower()
        viewMethod = request.parser_context["view"].action_map[requestMethod]

        if viewMethod not in request.authentication:
            return (None, None)

        if request.headers.get("Authorization", None) is None:
            raise AuthenticationFailedException({})

        bearerToken = request.headers.get("Authorization", None).split()[1]
        token = OAuthAccessTokenService().getByToken(bearerToken)

        if token.revoked_at is not None:
            raise AuthenticationFailedException({})

        owner = token.owner()
        return (owner, token)
