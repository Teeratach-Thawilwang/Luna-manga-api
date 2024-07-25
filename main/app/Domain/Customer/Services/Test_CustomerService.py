from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Customer.Models.CustomerFactory import CustomerFactory
from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from django.db import IntegrityError
from tests.TestCases import TestCases


class CustomerServiceTest(TestCases):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_findBy_name_should_success(self):
        params = {
            "email": "customer@email.com",
            "password": "some-password-hashed",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        customer = CustomerFactory.create(**params)

        param = {"email": "customer@email.com"}
        actual = CustomerService().findBy(param)

        self.assertEqual(1, actual.count())
        self.assertEqual(params["email"], list(actual)[0].email)
        self.assertEqual(params["first_name"], list(actual)[0].first_name)
        self.assertEqual(params["last_name"], list(actual)[0].last_name)

    def test_create_should_success(self):
        params = {
            "email": "customer@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        actual = CustomerService().create(params)

        self.assertEqual(params["email"], actual.email)
        self.assertEqual(params["first_name"], actual.first_name)
        self.assertEqual(params["last_name"], actual.last_name)

    def test_create_with_invalid_param_should_throw_exception(self):
        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(TypeError):
            CustomerService().create(params)

    def test_create_with_exist_email_should_throw_exception(self):
        params = {
            "email": "customer@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        customer = CustomerFactory.create(**params)

        with self.assertRaises(IntegrityError):
            CustomerService().create(params)

    def test_update_should_success(self):
        params = {
            "email": "customer@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        customer = CustomerFactory.create(**params)

        params["first_name"] = "new-first-name"
        actual = CustomerService().update(customer.id, params)

        self.assertEqual(params["email"], actual.email)
        self.assertEqual(params["first_name"], actual.first_name)
        self.assertEqual(params["last_name"], actual.last_name)

    def test_update_with_invalid_param_should_throw_exception(self):
        params = {
            "email": "customer@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        customer = CustomerFactory.create(**params)

        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(ResourceNotFoundException):
            CustomerService().update(customer.id, params)

    def test_update_with_exist_email_should_throw_exception(self):
        params1 = {
            "email": "customer1@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        customer1 = CustomerFactory.create(**params1)

        params2 = {
            "email": "customer2@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        customer2 = CustomerFactory.create(**params2)

        with self.assertRaises(ResourceNotFoundException):
            CustomerService().update(customer2.id, params1)

    def test_delete_should_success(self):
        params = {
            "email": "customer@email.com",
            "first_name": "some-first-name",
            "last_name": "some-last-name",
        }
        customer = CustomerFactory.create(**params)

        CustomerService().deleteById(customer.id)

        self.assertEqual(0, Customer.objects.all().count())
