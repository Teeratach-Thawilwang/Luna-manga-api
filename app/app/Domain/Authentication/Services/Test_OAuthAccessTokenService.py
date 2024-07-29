from app.Domain.Authentication.Models.OAuthAccessToken import OAuthAccessToken
from app.Domain.Authentication.Models.OAuthClientFactory import OAuthClientFactory
from app.Domain.Authentication.Services.OAuthAccessTokenService import OAuthAccessTokenService
from app.Domain.Customer.Models.CustomerFactory import CustomerFactory
from app.Domain.User.Models.UserFactory import UserFactory
from app.Exceptions.TokenExpiredException import TokenExpiredException
from app.Exceptions.TokenInvalidException import TokenInvalidException
from django.apps import apps
from django.utils import timezone
from tests.TestCases import TestCases


class OAuthAccessTokenServiceTest(TestCases):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_createGuestToken(self):
        self.setTestNow("2023-10-06 08:00:00")
        oAuthClient = OAuthClientFactory.create()

        actual = OAuthAccessTokenService().createGuestToken(oAuthClient.client_id)

        expected = timezone.now() + timezone.timedelta(days=1)
        self.assertEqual(expected, actual.expired_at)

    def test_createAccountToken_with_user(self):
        oAuthClient = OAuthClientFactory.create()
        user = UserFactory.create()

        actual = OAuthAccessTokenService().createAccountToken(oAuthClient.client_id, user)
        actual = OAuthAccessTokenService().createAccountToken(oAuthClient.client_id, user)
        actual = OAuthAccessTokenService().createAccountToken(oAuthClient.client_id, user)

        user.refresh_from_db()
        expectedToken = user.oAuthToken()

        self.assertIsInstance(actual.owner(), apps.get_model("app", "User"))
        self.assertEqual(expectedToken.access_token, actual.access_token)
        self.assertEqual(expectedToken.refresh_token, actual.refresh_token)

    def test_createAccountToken_with_customer(self):
        oAuthClient = OAuthClientFactory.create()
        customer = CustomerFactory.create()

        actual = OAuthAccessTokenService().createAccountToken(oAuthClient.client_id, customer)
        actual = OAuthAccessTokenService().createAccountToken(oAuthClient.client_id, customer)
        actual = OAuthAccessTokenService().createAccountToken(oAuthClient.client_id, customer)

        customer.refresh_from_db()
        expectedToken = customer.oAuthToken()

        self.assertIsInstance(actual.owner(), apps.get_model("app", "Customer"))
        self.assertEqual(expectedToken.access_token, actual.access_token)
        self.assertEqual(expectedToken.refresh_token, actual.refresh_token)

    def test_refreshToken_for_guest_when_refresh_token_not_expired(self):
        self.setTestNow("2023-10-06 08:00:00")
        token = self.createGuestToken()
        self.assertEqual(1, OAuthAccessToken.objects.all().count())

        self.setTestNow("2023-10-06 12:00:00")
        actual = OAuthAccessTokenService().refreshToken(token.refresh_token)

        self.assertEqual(2, OAuthAccessToken.objects.all().count())

        expectedCreatedAt = self.makeDateTimeFormat("2023-10-06 12:00:00").timestamp()
        self.assertEqual(expectedCreatedAt, actual.created_at.timestamp())

    def test_refreshToken_for_guest_when_refresh_token_expired(self):
        self.setTestNow("2023-10-01 08:00:00")
        token = self.createGuestToken()
        self.assertEqual(1, OAuthAccessToken.objects.all().count())

        self.setTestNow("2023-10-08 12:00:00")
        with self.assertRaises(TokenExpiredException):
            OAuthAccessTokenService().refreshToken(token.refresh_token)

    def test_refreshToken_for_user_when_refresh_token_not_expired(self):
        self.setTestNow("2023-10-06 08:00:00")
        token = self.createUserToken()
        self.assertEqual(1, OAuthAccessToken.objects.all().count())

        self.setTestNow("2023-10-06 12:00:00")
        actual = OAuthAccessTokenService().refreshToken(token.refresh_token)

        self.assertEqual(2, OAuthAccessToken.objects.all().count())

        expectedCreatedAt = self.makeDateTimeFormat("2023-10-06 12:00:00").timestamp()
        self.assertEqual(expectedCreatedAt, actual.created_at.timestamp())

    def test_refreshToken_for_user_when_refresh_token_expired(self):
        self.setTestNow("2023-10-01 08:00:00")
        token = self.createUserToken()
        self.assertEqual(1, OAuthAccessToken.objects.all().count())

        self.setTestNow("2023-10-08 12:00:00")
        with self.assertRaises(TokenExpiredException):
            OAuthAccessTokenService().refreshToken(token.refresh_token)

    def test_refreshToken_for_customer_when_refresh_token_not_expired(self):
        self.setTestNow("2023-10-06 08:00:00")
        token = self.createCustomerToken()
        self.assertEqual(1, OAuthAccessToken.objects.all().count())

        self.setTestNow("2023-10-06 12:00:00")
        actual = OAuthAccessTokenService().refreshToken(token.refresh_token)

        self.assertEqual(2, OAuthAccessToken.objects.all().count())

        expectedCreatedAt = self.makeDateTimeFormat("2023-10-06 12:00:00").timestamp()
        self.assertEqual(expectedCreatedAt, actual.created_at.timestamp())

    def test_refreshToken_for_customer_when_refresh_token_expired(self):
        self.setTestNow("2023-10-01 08:00:00")
        token = self.createCustomerToken()
        self.assertEqual(1, OAuthAccessToken.objects.all().count())

        self.setTestNow("2023-10-08 12:00:00")
        with self.assertRaises(TokenExpiredException):
            OAuthAccessTokenService().refreshToken(token.refresh_token)

    def test_refreshToken_when_refresh_token_revoked_already_should_throw_exception(self):
        self.setTestNow("2023-10-01 08:00:00")
        token = self.createCustomerToken()
        OAuthAccessTokenService().revokeToken(token.access_token)

        with self.assertRaises(TokenInvalidException):
            OAuthAccessTokenService().refreshToken(token.refresh_token)

    def test_revokeToken(self):
        token = self.createGuestToken()

        actual = OAuthAccessTokenService().revokeToken(token.access_token)
        self.assertIsNotNone(actual.revoked_at)
