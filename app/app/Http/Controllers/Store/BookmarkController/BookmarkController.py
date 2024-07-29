from app.Domain.Bookmark.Services.BookmarkService import BookmarkService
from app.Domain.Customer.Models.Customer import Customer
from app.Enums.StatusEnum import StoryStatusEnum
from app.Exceptions.PermissionException import PermissionException
from app.Http.Requests.Store.BookmarkController.DestroyRequest import DestroyRequest
from app.Http.Requests.Store.BookmarkController.IndexRequest import IndexRequest
from app.Http.Requests.Store.BookmarkController.StoreRequest import StoreRequest
from app.Http.Resources.Store.BookmarkController.BookmarkCollectionResource import BookmarkCollectionResource
from app.Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from django.http import HttpResponse
from rest_framework import status, viewsets


class BookmarkController(viewsets.ModelViewSet):
    authentication_classes = [AuthenticationMiddleware]

    def initial(self, request, *args, **kwargs):
        request.authentication = ["index", "store", "destroy"]
        super().initial(request, *args, **kwargs)

    def index(self, request):
        IndexRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        params = request.params
        params["story_status_in"] = [StoryStatusEnum.ONGOING, StoryStatusEnum.FINISHED]
        params["customer_id"] = customer.id

        if params["per_page"][0] == "all":
            params["per_page"][0] = 100

        paginated = BookmarkService().search(params).paginate()
        return BookmarkCollectionResource(paginated)

    def store(self, request):
        StoreRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        params = request.params
        params["customer_id"] = customer.id
        BookmarkService().create(params)

        return HttpResponse(status=status.HTTP_200_OK)

    def destroy(self, request):
        DestroyRequest(request)

        customer: Customer = request.user
        if customer == None:
            raise PermissionException({"message": "You have no permission."})

        params = request.params
        params["customer_id"] = customer.id
        BookmarkService().deleteBy(params)
        return HttpResponse(status=status.HTTP_200_OK)
