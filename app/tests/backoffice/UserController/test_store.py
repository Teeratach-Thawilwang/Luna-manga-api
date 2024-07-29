import json

from rest_framework import status
from rest_framework.test import APIClient
from tests.TestCases import TestCases


class StoreTest(TestCases):
    def setUp(self):
        super().setUp()
        self.url = "/backoffice/users"
        self.client = APIClient()
        admin = self.createAdmin()
        AuthToken = self.createUserToken(None, admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {AuthToken.access_token}")

    def tearDown(self):
        return super().tearDown()

    def test_store(self):
        params = {
            "email": "a@email.com",
            "first_name": "a",
            "last_name": "a",
            "password": "123456789",
        }

        response = self.client.post(self.route(), json.dumps(params), content_type="application/json")

        expected = {
            "email": "a@email.com",
            "first_name": "a",
            "last_name": "a",
            "password": "123456789",
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected["email"], response.data["email"])
        self.assertEqual(expected["first_name"], response.data["first_name"])
        self.assertEqual(expected["last_name"], response.data["last_name"])
