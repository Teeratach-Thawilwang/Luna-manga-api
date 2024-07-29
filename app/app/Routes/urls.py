from django.http import HttpResponse
from django.urls import include, path
from rest_framework import status


def healthCheck(request):
    return HttpResponse(status=status.HTTP_200_OK)


urlpatterns = [
    path("store/", include("app.Routes.store")),
    path("backoffice/", include("app.Routes.backoffice")),
    path("", healthCheck),
]
