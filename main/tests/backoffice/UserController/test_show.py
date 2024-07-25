import json

from app.Domain.User.Models.UserFactory import UserFactory
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from rest_framework import status
from rest_framework.test import APIClient
from tests.TestCases import TestCases


class ShowTest(TestCases):
    def setUp(self):
        super().setUp()
        self.url = "/backoffice/users"
        self.client = APIClient()
        admin = self.createAdmin()
        AuthToken = self.createUserToken(None, admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {AuthToken.access_token}")

    def tearDown(self):
        return super().tearDown()

    def test_show(self):
        params = {
            "email": "a@email.com",
            "first_name": "a",
            "last_name": "a",
            "password": "123456789",
        }
        user = UserFactory.create(**params)
        response = self.client.get(self.route(user.id))

        expected = {
            "email": "a@email.com",
            "first_name": "a",
            "last_name": "a",
            "password": "123456789",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected["email"], response.data["email"])
        self.assertEqual(expected["first_name"], response.data["first_name"])
        self.assertEqual(expected["last_name"], response.data["last_name"])

    def test_show_with_no_exist_user_should_throw_exception(self):
        userId = 999
        with self.assertRaisesMessage(ResourceNotFoundException, "User matching query does not exist."):
            self.client.get(self.route(userId))
