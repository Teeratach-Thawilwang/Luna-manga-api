from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Http.Requests.Backoffice.CustomerController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.CustomerController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.CustomerController.CustomerCollectionResource import CustomerCollectionResource
from app.Http.Resources.Backoffice.CustomerController.CustomerResource import CustomerResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from rest_framework import status, viewsets


class CustomerController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "update"]
        request.permissions = {
            "customer.view": ["index", "show"],
            "customer.manage": ["update"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = CustomerService().search(params).paginate()
        return CustomerCollectionResource(paginated)

    def show(self, request, id):
        customer = CustomerService().getById(id)
        return CustomerResource(customer, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        customer = CustomerService().update(id, params)

        return CustomerResource(customer, status=status.HTTP_200_OK)
