from app.Domain.User.Models.User import User
from app.Domain.User.Models.UserFactory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient
from tests.TestCases import TestCases


class DestroyTest(TestCases):
    def setUp(self):
        super().setUp()
        self.url = "/backoffice/users"
        self.client = APIClient()
        admin = self.createAdmin()
        AuthToken = self.createUserToken(None, admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {AuthToken.access_token}")

    def tearDown(self):
        return super().tearDown()

    def test_destroy(self):
        params = {
            "email": "a@email.com",
            "first_name": "a",
            "last_name": "a",
            "password": "123456789",
        }
        user = UserFactory.create(**params)
        response = self.client.delete(self.route(user.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, User.objects.filter(pk=user.id).count())
