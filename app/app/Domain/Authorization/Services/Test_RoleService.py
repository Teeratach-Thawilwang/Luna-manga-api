from app.Domain.Authorization.Models.PermissionFactory import PermissionFactory
from app.Domain.Authorization.Models.Role import Role
from app.Domain.Authorization.Models.RoleFactory import RoleFactory
from app.Domain.Authorization.Services.RoleService import RoleService
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from django.db import IntegrityError
from tests.TestCases import TestCases


class RoleServiceTest(TestCases):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_findBy_name_should_success(self):
        params = {
            "name": "admin",
            "guard_name": "backoffice",
            "description": "admin's role",
        }
        role = RoleFactory.create(**params)

        param = {"name": "admin"}
        actual = RoleService().findBy(param)

        self.assertEqual(1, actual.count())
        self.assertEqual(params["name"], list(actual)[0].name)
        self.assertEqual(params["guard_name"], list(actual)[0].guard_name)
        self.assertEqual(params["description"], list(actual)[0].description)

    def test_create_should_success(self):
        params = {
            "name": "admin",
            "guard_name": "backoffice",
            "description": "admin's role",
        }
        actual = RoleService().create(params)

        self.assertEqual(params["name"], actual.name)
        self.assertEqual(params["guard_name"], actual.guard_name)
        self.assertEqual(params["description"], actual.description)

    def test_create_with_invalid_param_should_throw_exception(self):
        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(TypeError):
            RoleService().create(params)

    def test_create_with_exist_name_should_throw_exception(self):
        params = {
            "name": "admin",
            "guard_name": "backoffice",
        }
        role = RoleFactory.create(**params)

        with self.assertRaises(IntegrityError):
            RoleService().create(params)

    def test_update_should_success(self):
        params = {
            "name": "normal user",
            "guard_name": "backoffice",
            "description": "admin's role",
        }
        role = RoleFactory.create(**params)

        params["name"] = "admin"
        actual = RoleService().update(role.id, params)

        self.assertEqual(params["name"], actual.name)
        self.assertEqual(params["guard_name"], actual.guard_name)
        self.assertEqual(params["description"], actual.description)

    def test_update_with_invalid_param_should_throw_exception(self):
        params = {
            "name": "normal user",
            "guard_name": "backoffice",
        }
        role = RoleFactory.create(**params)

        params = {"invalid-key": "invalid-key"}
        with self.assertRaises(ResourceNotFoundException):
            RoleService().update(role.id, params)

    def test_update_with_exist_name_should_throw_exception(self):
        params1 = {
            "name": "normal user 1",
            "guard_name": "backoffice",
        }
        role1 = RoleFactory.create(**params1)

        params2 = {
            "name": "normal user 2",
            "guard_name": "backoffice",
        }
        role2 = RoleFactory.create(**params2)

        with self.assertRaises(ResourceNotFoundException):
            RoleService().update(role2.id, params1)

    def test_delete_should_success(self):
        params = {
            "name": "normal user",
            "guard_name": "backoffice",
        }
        role = RoleFactory.create(**params)

        RoleService().deleteById(role.id)

        self.assertEqual(0, Role.objects.all().count())

    def test_add_permission_to_role(self):
        role = RoleFactory.create()
        permission = PermissionFactory.create()

        self.assertQuerySetEqual([], role.permissions())

        role.permission().add(permission)
        self.assertEqual(role.permissions().first().data(), permission.data())

    def test_remove_permission_for_role(self):
        role = RoleFactory.create()
        permission = PermissionFactory.create()
        role.permission().add(permission)

        self.assertEqual(role.permissions().first().data(), permission.data())

        role.permission().remove(permission)
        self.assertQuerySetEqual([], role.permissions())

    def test_clear_all_permission_for_role(self):
        role = RoleFactory.create()
        permission = PermissionFactory.create()
        role.permission().add(permission)

        self.assertEqual(role.permissions().first().data(), permission.data())

        role.permission().clear()
        self.assertQuerySetEqual([], role.permissions())

    def test_sync_permission(self):
        role = RoleFactory.create()
        permission1 = PermissionFactory.create()
        permission2 = PermissionFactory.create()
        permission3 = PermissionFactory.create()

        role.permission().add(permission1)
        self.assertEqual(role.permissions().first().data(), permission1.data())

        permissionIds = [
            permission2.id,
            permission3.id,
        ]
        RoleService().syncPermission(role.id, permissionIds)

        permissions = role.permissions().all()
        self.assertEqual(2, permissions.count())
        self.assertEqual(permission2.data(), permissions[0].data())
        self.assertEqual(permission3.data(), permissions[1].data())
