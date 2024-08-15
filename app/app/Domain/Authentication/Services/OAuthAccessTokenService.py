import uuid
from sys import modules
from typing import Any

import jwt
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from app.Domain.Authentication.Models.OAuthAccessToken import OAuthAccessToken
from app.Domain.Authentication.Models.OAuthClient import OAuthClient
from app.Domain.Customer.Models.Customer import Customer
from app.Domain.User.Models.User import User
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Exceptions.TokenExpiredException import TokenExpiredException
from app.Exceptions.TokenInvalidException import TokenInvalidException
from app.Services.Helpers import getDatetimeTodayUtc

if "OAuthClientService" not in modules:
    from app.Domain.Authentication.Services.OAuthClientService import OAuthClientService


class OAuthAccessTokenService:
    def getBy(self, params: dict[str, Any]) -> OAuthAccessToken:
        try:
            return OAuthAccessToken.objects.filter(**params).get()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def generateToken(self, oAuthClient: OAuthClient, account: Customer | User = None) -> dict[str, Any]:
        uuid4 = str(uuid.uuid4())
        issueAt = timezone.now()
        midnighTodaytUTC = getDatetimeTodayUtc()

        accessTokenExpiredAt = midnighTodaytUTC + timezone.timedelta(days=1)
        refreshTokenExpiredAt = midnighTodaytUTC + timezone.timedelta(days=7)

        payload = {
            "uuid": uuid4,
            "client_id": oAuthClient.client_id,
            "created_at": issueAt.timestamp(),
        }

        accessTokenPayload = payload
        refreshTokenPayload = payload

        accessTokenPayload["expired_at"] = accessTokenExpiredAt.timestamp()
        refreshTokenPayload["expired_at"] = refreshTokenExpiredAt.timestamp()

        if account is not None:
            contentType = ContentType.objects.get_for_model(account)
            accessTokenPayload["model_id"] = account.id
            accessTokenPayload["model_type"] = contentType.id

            refreshTokenPayload["model_id"] = account.id
            refreshTokenPayload["model_type"] = contentType.id

        accessToken = jwt.encode(accessTokenPayload, oAuthClient.client_secret, algorithm="HS256")
        refreshToken = jwt.encode(refreshTokenPayload, oAuthClient.client_secret, algorithm="HS256")

        token = {
            "access_token": accessToken,
            "refresh_token": refreshToken,
            "expired_at": accessTokenExpiredAt,
        }
        return token

    def createGuestToken(self, clientId: str, meta: dict[str]) -> OAuthAccessToken:
        oAuthClient = OAuthClientService().getByClientId(clientId)
        token = self.generateToken(oAuthClient)
        params = {
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "scopes": "read",
            "expired_at": token["expired_at"],
            "client_id": oAuthClient.id,
            "meta": meta,
        }

        return OAuthAccessToken.objects.create(**params)

    def createAccountToken(self, clientId: str, account: Customer | User, meta: dict[str]) -> OAuthAccessToken:
        oAuthClient = OAuthClientService().getByClientId(clientId)
        token = self.generateToken(oAuthClient, account)
        params = {
            "model_id": account.id,
            "model_type": ContentType.objects.get_for_model(account),
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "scopes": "read write",
            "expired_at": token["expired_at"],
            "client_id": oAuthClient.id,
            "meta": meta,
        }

        return OAuthAccessToken.objects.create(**params)

    def getByToken(self, token: str) -> OAuthAccessToken:
        oAuthAccessToken = self.getBy({"access_token": token})
        accessTokenPayload = self.decodeToken(oAuthAccessToken)

        if not self.isValidTokenFormat(accessTokenPayload):
            raise TokenInvalidException({})

        if accessTokenPayload["client_id"] != oAuthAccessToken.client.client_id:
            raise TokenInvalidException({})

        if self.isExpired(oAuthAccessToken.expired_at.timestamp()):
            raise TokenExpiredException({})

        return oAuthAccessToken

    def decodeToken(self, oAuthAccessToken: OAuthAccessToken) -> Any:
        oAuthClient: OAuthClient = oAuthAccessToken.client
        return jwt.decode(oAuthAccessToken.access_token, oAuthClient.client_secret, algorithms="HS256")

    def isExpired(self, timeStamp: float):
        timeNow = timezone.now().timestamp()
        return timeNow > timeStamp

    def isValidTokenFormat(self, token: Any) -> bool:
        if ("uuid" in token) and ("created_at" in token) and ("expired_at" in token):
            return True
        return False

    def refreshToken(self, refreshToken: str, meta: dict[str]) -> OAuthAccessToken:
        oAuthAccessToken = self.getBy({"refresh_token": refreshToken})

        if oAuthAccessToken.revoked_at is not None:
            raise TokenInvalidException({})

        refreshTokenExpiredAt = oAuthAccessToken.created_at + timezone.timedelta(days=7)
        if self.isExpired(refreshTokenExpiredAt.timestamp()):
            raise TokenExpiredException({})

        clientId = oAuthAccessToken.client.client_id

        if oAuthAccessToken.model is not None:
            account = oAuthAccessToken.owner()
            return self.createAccountToken(clientId, account, meta)

        return self.createGuestToken(clientId, meta)

    def revokeToken(self, token: str) -> OAuthAccessToken:
        params = {
            "revoked_at": timezone.now(),
            "updated_at": timezone.now(),
        }
        try:
            OAuthAccessToken.objects.filter(access_token=token).update(**params)
            return self.getBy({"access_token": token})
        except Exception as e:
            raise ResourceNotFoundException({"message": e})
