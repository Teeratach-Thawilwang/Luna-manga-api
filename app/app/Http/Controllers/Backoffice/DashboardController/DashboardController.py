from app.Domain.Dashboard.Services.DashboardService import DashboardService
from app.Http.Resources.Backoffice.DashboardController.DashboardResource import DashboardResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from rest_framework import status, viewsets


class DashboardController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["show"]
        super().initial(request, *args, **kwargs)

    def show(self, request):
        items = DashboardService().createDashboardItems()
        return DashboardResource(items, status=status.HTTP_200_OK)
