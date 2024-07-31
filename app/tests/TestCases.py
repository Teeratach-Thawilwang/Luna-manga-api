import re
from datetime import datetime

from app.Domain.Authentication.Models.OAuthClientFactory import OAuthClientFactory
from app.Domain.Authentication.Services.OAuthAccessTokenService import OAuthAccessTokenService
from app.Domain.Authorization.Models.Permission import Permission
from app.Domain.Authorization.Models.PermissionFactory import PermissionFactory
from app.Domain.Authorization.Models.RoleFactory import RoleFactory
from app.Domain.Customer.Models.CustomerFactory import CustomerFactory
from app.Domain.User.Models.UserFactory import UserFactory
from app.Settings.permission import permission as defaultPermissions
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from freezegun import freeze_time


class TestCases(TestCase):
    def setUp(self):
        self.pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        self.initialPermission()
        return super().setUp()

    def tearDown(self):
        if hasattr(self, "freezer"):
            self.freezer.stop()
        return super().tearDown()

    def setTestNow(self, dateTimeString):
        # This approach makes unit-test run slower about 0.009 seconds.
        self.validateDateTimeFormat(dateTimeString)
        self.freezer = freeze_time(dateTimeString)
        self.freezer.start()

    def now(self):
        return datetime.now()

    def nowFormat(self, formatString="%Y-%m-%d %H:%M:%S"):
        return datetime.now().strftime(formatString)

    def makeDateTimeFormat(self, dateTimeString):
        self.validateDateTimeFormat(dateTimeString)
        return datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S")

    def validateDateTimeFormat(self, dateTimeString):
        if not re.match(self.pattern, dateTimeString):
            raise Exception('datetime should be "%Y-%m-%d %H:%M:%S" format.')

    def route(self, slug=None):
        if slug:
            return self.url + f"/{slug}"
        return self.url

    def createGuestToken(self, oAuthClient=None):
        if oAuthClient is None:
            oAuthClient = OAuthClientFactory.create(**{"name": "client app"})
        return OAuthAccessTokenService().createGuestToken(oAuthClient.client_id)

    def createUserToken(self, oAuthClient=None, user=None):
        if oAuthClient is None:
            oAuthClient = OAuthClientFactory.create(**{"name": "client app"})
        if user is None:
            user = UserFactory.create()
        return OAuthAccessTokenService().createAccountToken(oAuthClient.client_id, user)

    def createCustomerToken(self, oAuthClient=None, customer=None):
        if oAuthClient is None:
            oAuthClient = OAuthClientFactory.create(**{"name": "client app"})
        if customer is None:
            customer = CustomerFactory.create()
        return OAuthAccessTokenService().createAccountToken(oAuthClient.client_id, customer)

    def addRolePermisionToModel(self, model, role, permission):
        role.permissions().add(permission)
        params = {
            "role_id": role.id,
            "model_type": ContentType.objects.get_for_model(model),
            "model_id": model.id,
        }
        role.modelHasRoles().create(**params)

    def initialPermission(self):
        for key, value in defaultPermissions.items():
            PermissionFactory.create(**{"name": key, "guard_name": "backoffice"})

    def createAdmin(self, isSuperUser=False):
        user = UserFactory.create(**{"is_superuser": isSuperUser})
        role = RoleFactory.create(**{"guard_name": "backoffice", "name": "admin"})
        permissions = Permission.objects.all()

        for permission in permissions:
            role.permission().add(permission)

        params = {
            "role_id": role.id,
            "model_type": ContentType.objects.get_for_model(user),
            "model_id": user.id,
        }
        role.modelHasRoles().create(**params)
        return user
