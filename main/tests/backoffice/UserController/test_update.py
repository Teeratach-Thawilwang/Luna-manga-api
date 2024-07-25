import json

from app.Domain.User.Models.UserFactory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient
from tests.TestCases import TestCases


class UpdateTest(TestCases):
    def setUp(self):
        super().setUp()
        self.url = "/backoffice/users"
        self.client = APIClient()
        admin = self.createAdmin()
        AuthToken = self.createUserToken(None, admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {AuthToken.access_token}")

    def tearDown(self):
        return super().tearDown()

    def test_update(self):
        params = {
            "email": "a@email.com",
            "first_name": "a",
            "last_name": "a",
        }
        user = UserFactory.create(**params)

        params["first_name"] = "new first name"

        response = self.client.put(self.route(user.id), json.dumps(params), content_type="application/json")

        expected = {
            "email": "a@email.com",
            "first_name": "new first name",
            "last_name": "a",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected["email"], response.data["email"])
        self.assertEqual(expected["first_name"], response.data["first_name"])
        self.assertEqual(expected["last_name"], response.data["last_name"])
