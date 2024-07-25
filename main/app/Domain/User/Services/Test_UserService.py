from app.Domain.User.Models.User import User
from app.Domain.User.Models.UserFactory import UserFactory
from app.Domain.User.Services.UserService import UserService
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from django.db import IntegrityError
from tests.TestCases import TestCases


class UserServiceTest(TestCases):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_findBy_name_should_success(self):
        params = {
            "email": "user@email.com",
            "password": "some-password-hashed",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
            "is_superuser": False,
        }
        user = UserFactory.create(**params)

        param = {"email": "user@email.com"}
        actual = UserService().findBy(param)

        self.assertEqual(1, actual.count())
        self.assertEqual(params["email"], list(actual)[0].email)
        self.assertEqual(params["first_name"], list(actual)[0].first_name)
        self.assertEqual(params["last_name"], list(actual)[0].last_name)

    def test_create_should_success(self):
        params = {
            "email": "user@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        actual = UserService().create(params)

        self.assertEqual(params["email"], actual.email)
        self.assertEqual(params["first_name"], actual.first_name)
        self.assertEqual(params["last_name"], actual.last_name)

    def test_create_with_invalid_param_should_throw_exception(self):
        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(TypeError):
            UserService().create(params)

    def test_create_with_exist_email_should_throw_exception(self):
        params = {
            "email": "user@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        user = UserFactory.create(**params)

        with self.assertRaises(IntegrityError):
            UserService().create(params)

    def test_update_should_success(self):
        params = {
            "email": "user@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        user = UserFactory.create(**params)

        params["first_name"] = "new-first-name"
        actual = UserService().update(user.id, params)

        self.assertEqual(params["email"], actual.email)
        self.assertEqual(params["first_name"], actual.first_name)
        self.assertEqual(params["last_name"], actual.last_name)

    def test_update_with_invalid_param_should_throw_exception(self):
        params = {
            "email": "user@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        user = UserFactory.create(**params)

        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(ResourceNotFoundException):
            UserService().update(user.id, params)

    def test_update_with_exist_email_should_throw_exception(self):
        params1 = {
            "email": "user1@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        user1 = UserFactory.create(**params1)

        params2 = {
            "email": "user2@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        user2 = UserFactory.create(**params2)

        with self.assertRaises(ResourceNotFoundException):
            UserService().update(user2.id, params1)

    def test_delete_should_success(self):
        params = {
            "email": "user@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        user = UserFactory.create(**params)

        UserService().deleteById(user.id)

        self.assertEqual(0, User.objects.all().count())
