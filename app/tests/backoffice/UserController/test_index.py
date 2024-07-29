from app.Domain.User.Models.UserFactory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient
from tests.TestCases import TestCases


class IndexTest(TestCases):
    def setUp(self):
        super().setUp()
        self.url = "/backoffice/users"
        self.client = APIClient()
        admin = self.createAdmin()
        AuthToken = self.createUserToken(None, admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {AuthToken.access_token}")

    def tearDown(self):
        return super().tearDown()

    def test_index(self):
        for i in range(10):
            UserFactory.create()

        params = {
            "page": 1,
            "per_page": 4,
        }
        response = self.client.get(self.route(), params)

        expected = {
            "current": 1,
            "next": 2,
            "previous": None,
            "last": 3,
            "total": 11,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected["current"], response.data["current"])
        self.assertEqual(expected["next"], response.data["next"])
        self.assertEqual(expected["previous"], response.data["previous"])
        self.assertEqual(expected["last"], response.data["last"])
        self.assertEqual(expected["total"], response.data["total"])
        self.assertIn("data", response.data)
