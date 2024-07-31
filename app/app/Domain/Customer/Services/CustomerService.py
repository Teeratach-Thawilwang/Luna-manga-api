from sys import modules
from typing import Any

from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone

from app.Domain.Customer.Models.Customer import Customer
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Enums.StatusEnum import CustomerStatusEnum
from app.Exceptions.InActiveAccountException import InActiveAccountException
from app.Exceptions.PasswordInvalidException import PasswordInvalidException
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate

if "FileableService" not in modules:
    from app.Domain.File.Services.FileableService import FileableService


class CustomerService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id", "email"]
        self.querySet = Customer.objects

    def getAll(self) -> QuerySet:
        return self.querySet.all()

    def getById(self, id: int) -> Customer:
        try:
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def getByEmail(self, email: str) -> Customer:
        try:
            return self.querySet.get(email=email)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return self.querySet.filter(**params)

    def create(self, params: dict[str, Any]) -> Customer:
        params["status"] = CustomerStatusEnum.INACTIVE

        if "password" in params:
            params["password"] = make_password(params["password"])

        return self.querySet.create(**params)

    def update(self, id: int, params: dict[str, Any]) -> Customer:
        imageId = None
        params["updated_at"] = timezone.now()

        if "password" in params:
            params["password"] = make_password(params["password"])

        if "profile_image_id" in params:
            imageId = params["profile_image_id"]
            del params["profile_image_id"]

        try:
            self.querySet.filter(pk=id).update(**params)
            if imageId != None:
                FileableService().syncSingleFileable(id, "customer", imageId, CollectionNameEnum.PROFILE_IMAGE)
            return self.querySet.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def prefetch(self, *relations: tuple):
        self.querySet = self.querySet.prefetch_related(*relations)
        return self

    def search(self, params: dict[str, Any]):
        if "q" in params:
            q: str = params["q"][0]
            if q.isnumeric():
                self.query += [Q(id__exact=q)]
            else:
                self.query += [Q(email__istartswith=q) | Q(first_name__istartswith=q)]

        if "status" in params:
            self.query += [Q(status__exact=params["status"][0])]

        if "start_date" in params:
            self.query += [Q(created_at__gte=params["start_date"][0])]

        if "end_date" in params:
            self.query += [Q(created_at__lte=params["end_date"][0])]

        if "page" in params:
            self.page = int(params["page"][0])

        if "per_page" in params:
            self.perPage = int(params["per_page"][0])

        if "order_by" in params:
            self.orderBy = params["order_by"]

        return self

    def paginate(self) -> list:
        self.prefetch("customer_group", "fileable__file", "story_set")
        return paginate(self.page, self.perPage, self.querySet, self.query, self.orderBy)

    def checkPassword(self, customer: Customer, password: str) -> None:
        if not check_password(password, customer.password):
            raise PasswordInvalidException({"message": "Password Invalid"})

    def isActive(self, customer: Customer) -> bool:
        return customer.status == CustomerStatusEnum.ACTIVE

    def isDelete(self, customer: Customer) -> bool:
        return customer.is_deleted

    def isVerifiedEmail(self, customer: Customer) -> bool:
        return customer.email_verified_at != None

    def checkActiveUser(self, customer: Customer) -> None:
        if not self.isActive(customer):
            raise InActiveAccountException({"message": "Inactive Account"})

    def emailVerified(self, customer: Customer) -> None:
        customer.status = CustomerStatusEnum.ACTIVE
        customer.email_verified_at = timezone.now()
        customer.updated_at = timezone.now()
        customer.save()

    def resetPassword(self, customer: Customer, password: str) -> None:
        customer.password = make_password(password)
        customer.updated_at = timezone.now()
        customer.save()
