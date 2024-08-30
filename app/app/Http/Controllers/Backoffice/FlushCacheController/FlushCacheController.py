from django.http import HttpResponse
from rest_framework import status, viewsets

from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Services.Helpers import flushCache


class FlushCacheController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index"]
        super().initial(request, *args, **kwargs)

    def index(self, request):
        flushCache()
        return HttpResponse(status=status.HTTP_200_OK)
