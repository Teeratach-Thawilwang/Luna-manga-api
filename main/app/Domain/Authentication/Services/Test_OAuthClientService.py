from app.Domain.Authentication.Models.OAuthClientFactory import OAuthClientFactory
from app.Domain.Authentication.Services.OAuthClientService import OAuthClientService
from tests.TestCases import TestCases


class OAuthClientServiceTest(TestCases):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_create(self):
        param = {"name": "mobile app - oauth client"}
        actaul = OAuthClientService().create(param)

        self.assertEqual(param["name"], actaul.name)
        self.assertIsNotNone(actaul.client_id)
        self.assertIsNotNone(actaul.client_secret)
        self.assertIsNone(actaul.redirect_url)

    def test_getByClientId(self):
        oAuthClient1 = OAuthClientFactory.create()
        oAuthClient2 = OAuthClientFactory.create()
        oAuthClient3 = OAuthClientFactory.create()
        oAuthClient4 = OAuthClientFactory.create()

        actaul = OAuthClientService().getByClientId(oAuthClient3.client_id)

        self.assertEqual(oAuthClient3.name, actaul.name)
        self.assertEqual(oAuthClient3.client_id, actaul.client_id)
        self.assertEqual(oAuthClient3.client_secret, actaul.client_secret)
        self.assertEqual(oAuthClient3.redirect_url, actaul.redirect_url)
