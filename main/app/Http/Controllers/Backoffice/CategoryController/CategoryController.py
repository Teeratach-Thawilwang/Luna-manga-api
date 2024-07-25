from app.Domain.Category.Services.CategoryService import CategoryService
from app.Http.Requests.Backoffice.CategoryController.IndexRequest import IndexRequest
from app.Http.Requests.Backoffice.CategoryController.StoreRequest import StoreRequest
from app.Http.Requests.Backoffice.CategoryController.UpdateRequest import UpdateRequest
from app.Http.Resources.Backoffice.CategoryController.CategoryCollectionResource import CategoryCollectionResource
from app.Http.Resources.Backoffice.CategoryController.CategoryResource import CategoryResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from app.Middlewares.UserPermissionMiddleware import UserPermissionMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class CategoryController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [UserPermissionMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "show", "store", "update", "destroy"]
        request.permissions = {
            "category.view": ["index", "show"],
            "category.manage": ["store", "update", "destroy"],
        }
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        params = request.params
        paginated = CategoryService().search(params).paginate()
        return CategoryCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        params = request.params
        user = CategoryService().create(params)

        return CategoryResource(user, status=status.HTTP_201_CREATED)

    def show(self, request, id):
        user = CategoryService().getById(id)
        return CategoryResource(user, status=status.HTTP_200_OK)

    def update(self, request, id):
        UpdateRequest(request)

        params = request.params
        user = CategoryService().update(id, params)

        return CategoryResource(user, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        CategoryService().deleteById(id)
        return HttpResponse(status=status.HTTP_200_OK)
