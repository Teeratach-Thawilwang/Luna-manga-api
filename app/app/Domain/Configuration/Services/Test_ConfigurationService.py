from app.Domain.Configuration.Models.Configuration import Configuration
from app.Domain.Configuration.Models.ConfigurationFactory import ConfigurationFactory
from app.Domain.Configuration.Services.ConfigurationService import ConfigurationService
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from django.core.exceptions import FieldDoesNotExist
from django.db import IntegrityError
from tests.TestCases import TestCases


class ConfigurationServiceTest(TestCases):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_findBy_key_should_success(self):
        params = {"key": "some-key", "value": "some-value"}
        ConfigurationFactory.create(**params)

        param = {"key": "some-key"}
        actual = ConfigurationService().findBy(param)

        self.assertEqual(1, actual.count())
        self.assertEqual(params["key"], list(actual)[0].key)
        self.assertEqual(params["value"], list(actual)[0].value)

    def test_findBy_value_should_success(self):
        params = {"key": "key-1", "value": "some-value"}
        ConfigurationFactory.create(**params)

        params = {"key": "key-2", "value": "some-value"}
        ConfigurationFactory.create(**params)

        param = {"value": "some-value"}
        actual = ConfigurationService().findBy(param)

        self.assertEqual(2, actual.count())
        self.assertEqual("key-1", list(actual)[0].key)
        self.assertEqual("key-2", list(actual)[1].key)

    def test_create_should_success(self):
        params = {"key": "some-key", "value": "some-value"}
        actual = ConfigurationService().create(params)
        self.assertEqual(params["key"], actual.key)
        self.assertEqual(params["value"], actual.value)

    def test_create_with_invalid_param_should_throw_exception(self):
        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(TypeError):
            ConfigurationService().create(params)

    def test_create_with_exist_key_should_throw_exception(self):
        params = {"key": "some-key", "value": "some-value"}
        ConfigurationFactory.create(**params)

        with self.assertRaises(IntegrityError):
            ConfigurationService().create(params)

    def test_update_should_success(self):
        params = {"key": "some-key", "value": "some-value"}
        configuration = ConfigurationFactory.create(**params)

        params["key"] = "new-key"
        actual = ConfigurationService().update(configuration.id, params)
        self.assertEqual(params["key"], actual.key)
        self.assertEqual(params["value"], actual.value)

    def test_update_with_invalid_param_should_throw_exception(self):
        params = {"key": "some-key", "value": "some-value"}
        configuration = ConfigurationFactory.create(**params)

        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(ResourceNotFoundException):
            ConfigurationService().update(configuration.id, params)

    def test_update_with_exist_key_should_throw_exception(self):
        params1 = {"key": "exist-key", "value": "some-value"}
        configuration = ConfigurationFactory.create(**params1)

        params2 = {"key": "other-key", "value": "some-value"}
        configuration = ConfigurationFactory.create(**params2)

        with self.assertRaises(ResourceNotFoundException):
            ConfigurationService().update(configuration, params1)

    def test_delete_should_success(self):
        params = {"key": "exist-key", "value": "some-value"}
        configuration = ConfigurationFactory.create(**params)

        ConfigurationService().deleteById(configuration.id)

        self.assertEqual(0, Configuration.objects.all().count())
