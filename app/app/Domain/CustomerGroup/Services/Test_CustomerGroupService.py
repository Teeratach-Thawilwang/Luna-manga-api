from app.Domain.Customer.Models.CustomerFactory import CustomerFactory
from app.Domain.Customer.Services.CustomerService import CustomerService
from app.Domain.CustomerGroup.Models.CustomerGroup import CustomerGroup
from app.Domain.CustomerGroup.Models.CustomerGroupFactory import CustomerGroupFactory
from app.Domain.CustomerGroup.Services.CustomerGroupService import CustomerGroupService
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from django.db import IntegrityError
from tests.TestCases import TestCases


class CustomerGroupServiceTest(TestCases):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_findBy_name_should_success(self):
        param = {"name": "group_name"}
        customerGroup = CustomerGroupFactory.create(**param)

        param = {"name": "group_name"}
        actual = CustomerGroupService().findBy(param)

        self.assertEqual(1, actual.count())
        self.assertEqual("group_name", list(actual)[0].name)

    def test_create_should_success(self):
        params = {
            "name": "group_name",
        }
        actual = CustomerGroupService().create(params)

        self.assertEqual(params["name"], actual.name)

    def test_create_with_invalid_param_should_throw_exception(self):
        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(TypeError):
            CustomerGroupService().create(params)

    def test_create_with_exist_name_should_throw_exception(self):
        params = {
            "name": "group_name",
        }
        customerGroup = CustomerGroupFactory.create(**params)

        with self.assertRaises(IntegrityError):
            CustomerGroupService().create(params)

    def test_update_should_success(self):
        params = {
            "name": "group_name",
        }
        customerGroup = CustomerGroupFactory.create(**params)

        params["name"] = "new_group_name"
        actual = CustomerGroupService().update(customerGroup.id, params)

        self.assertEqual(params["name"], actual.name)

    def test_update_with_invalid_param_should_throw_exception(self):
        params = {
            "name": "group_name",
        }
        customerGroup = CustomerGroupFactory.create(**params)

        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(ResourceNotFoundException):
            CustomerGroupService().update(customerGroup.id, params)

    def test_update_with_exist_name_should_throw_exception(self):
        params1 = {
            "name": "group_name1",
        }
        customerGroup1 = CustomerGroupFactory.create(**params1)

        params2 = {
            "name": "group_name2",
        }
        customerGroup2 = CustomerGroupFactory.create(**params2)

        with self.assertRaises(ResourceNotFoundException):
            CustomerGroupService().update(customerGroup2.id, params1)

    def test_delete_should_success(self):
        params = {
            "name": "group_name",
        }
        customerGroup = CustomerGroupFactory.create(**params)

        CustomerGroupService().deleteById(customerGroup.id)

        self.assertEqual(0, CustomerGroup.objects.all().count())

    def test_model_relation_to_customer_model(self):
        customerGroup = CustomerGroupFactory.create()
        customer = CustomerFactory.create()
        customer.group().add(customerGroup)

        customerGroupsActual = CustomerGroupService().findBy({"id": customerGroup.id})
        customerGroupActual = customerGroupsActual.first()

        customerActual = customerGroupActual.customer_set.all().first()

        self.assertEqual(customer, customerActual)
        self.assertEqual(customer.id, customerActual.id)
        self.assertEqual(customer.email, customerActual.email)

    def test_delete_group_should_set_group_to_null_for_customer_in_the_group(self):
        customerGroup = CustomerGroupFactory.create()
        customer = CustomerFactory.create()
        customer.group().add(customerGroup)

        CustomerGroupService().deleteById(customerGroup.id)

        customer = CustomerService().findBy({"id": customer.id}).first()
        self.assertEqual(0, customer.group().count())
