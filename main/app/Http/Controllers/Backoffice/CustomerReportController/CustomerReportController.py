from app.Domain.CustomerReport.Services.CustomerReportService import CustomerReportService
from app.Http.Requests.Backoffice.CustomerReportController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.CustomerReportController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.CustomerReportController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.CustomerReportController.CustomerReportCollectionResource import CustomerReportCollectionResource
from app.Http.Resources.Backoffice.CustomerReportController.CustomerReportResource import CustomerReportResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class CustomerReportController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "customer_report.view": ["index", "show"],
            "customer_report.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = CustomerReportService().search(params).paginate()
        return CustomerReportCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params = request.params
        customerReport = CustomerReportService().create(params)

        return CustomerReportResource(customerReport, status=status.HTTP_201_CREATED)

    def show(self, request, id):
        customerReport = CustomerReportService().getById(id)
        return CustomerReportResource(customerReport, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        params["accept_by"] = request.user
        customerReport = CustomerReportService().update(id, params)

        return CustomerReportResource(customerReport, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        CustomerReportService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
