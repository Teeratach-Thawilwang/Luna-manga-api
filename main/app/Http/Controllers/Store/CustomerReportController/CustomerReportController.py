from app.Domain.Customer.Models.Customer import Customer
from app.Domain.CustomerReport.Services.CustomerReportService import CustomerReportService
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.CustomerReportController.StoreRequest import StoreRequest
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class CustomerReportController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["store"]
        super().initial(request, *args, **kwargs)

    def store(self, request):
        StoreRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        params = request.params
        CustomerReportService().create(params)

        return HttpResponse(status=status.HTTP_201_CREATED)
