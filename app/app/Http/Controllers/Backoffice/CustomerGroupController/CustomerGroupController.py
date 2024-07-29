from app.Domain.CustomerGroup.Services.CustomerGroupService import CustomerGroupService
from app.Http.Requests.Backoffice.CustomerGroupController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.CustomerGroupController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.CustomerGroupController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.CustomerGroupController.CustomerGroupCollectionResource import CustomerGroupCollectionResource
from app.Http.Resources.Backoffice.CustomerGroupController.CustomerGroupResource import CustomerGroupResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class CustomerGroupController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "customer_group.view": ["index", "show"],
            "customer_group.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = CustomerGroupService().search(params).paginate()
        return CustomerGroupCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params = request.params
        customerGroup = CustomerGroupService().create(params)

        return CustomerGroupResource(customerGroup, status=status.HTTP_201_CREATED)

    def show(self, request, id):
        customerGroup = CustomerGroupService().getById(id)
        return CustomerGroupResource(customerGroup, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        customerGroup = CustomerGroupService().update(id, params)

        return CustomerGroupResource(customerGroup, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        CustomerGroupService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
