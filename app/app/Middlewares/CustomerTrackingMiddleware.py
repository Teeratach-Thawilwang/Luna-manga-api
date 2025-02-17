import functools
import json

from app.Domain.Authentication.Services.OAuthAccessTokenService import OAuthAccessTokenService
from app.Domain.Customer.Models.Customer import Customer
from app.Domain.CustomerTracking.Services.CustomerTrackingService import CustomerTrackingService


def CustomerTrackingMiddleware(next):
    @functools.wraps(next)
    def wrapper(request, *args, **kwargs):
        if request.headers.get("Authorization", None) is None:
            return next(request, *args, **kwargs)

        bearerToken = request.headers.get("Authorization", None).split()[1]
        try:
            token = OAuthAccessTokenService().getByToken(bearerToken)
            owner = token.owner()
        except:
            return next(request, *args, **kwargs)

        if isinstance(owner, Customer):
            params = {
                "customer": owner,
                "token": token,
                "request_url": request.path_info,
            }
            CustomerTrackingService().create(params)
        return next(request, *args, **kwargs)

    return wrapper
