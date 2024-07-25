from typing import Any

from app.Domain.User.Models.User import User
from app.Enums.StatusEnum import UserStatusEnum
from app.Exceptions.InActiveAccountException import InActiveAccountException
from app.Exceptions.PasswordInvalidException import PasswordInvalidException
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from app.Services.Paginator import paginate
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone


class UserService:
    def __init__(self):
        self.page = 1
        self.perPage = 15
        self.query = []
        self.orderBy = ["-id", "email"]

    def getAll(self) -> QuerySet:
        return User.objects.all()

    def getById(self, id) -> User:
        try:
            return User.objects.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def getByEmail(self, email) -> User:
        try:
            return User.objects.get(email=email)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return User.objects.filter(**params)

    def create(self, params: dict[str, Any]) -> User:
        if "password" in params:
            params["password"] = make_password(params["password"])

        return User.objects.create(**params)

    def update(self, id: int, params: dict[str, Any]) -> User:
        params["updated_at"] = timezone.now()
        if "password" in params:
            params["password"] = make_password(params["password"])

        try:
            User.objects.filter(pk=id).update(**params)
            return User.objects.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteById(self, id) -> None:
        try:
            user = User.objects.get(pk=id)
            user.delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def search(self, params):
        if "q" in params:
            q: str = params["q"][0]
            if q.isnumeric():
                self.query += [Q(id__exact=q)]
            else:
                self.query += [Q(email__startswith=q) | Q(first_name__startswith=q)]

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
        return paginate(self.page, self.perPage, User.objects, self.query, self.orderBy)

    def checkPassword(self, user: User, password: str):
        if not check_password(password, user.password):
            raise PasswordInvalidException({"message": "Password Invalid"})

    def isActive(self, user: User):
        return user.status == UserStatusEnum.ACTIVE and not user.is_deleted

    def checkActiveUser(self, user: User):
        if not self.isActive(user):
            raise InActiveAccountException({"message": "Inactive Account"})
