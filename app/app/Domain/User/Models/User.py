from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=150, db_index=True)
    password = models.CharField(max_length=150)
    nick_name = models.CharField(max_length=30, null=True, default=None, db_collation="utf8mb4_unicode_ci")
    first_name = models.CharField(max_length=150, db_collation="utf8mb4_unicode_ci")
    last_name = models.CharField(max_length=150, db_collation="utf8mb4_unicode_ci")
    phone_number = models.CharField(max_length=20, null=True, default=None)
    is_superuser = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default="inactive")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, default=None)
    is_deleted = models.BooleanField(default=False)

    oauth_access_token = GenericRelation("OAuthAccessToken", content_type_field="model_type", object_id_field="model_id")
    model_has_role = GenericRelation("ModelHasRole", content_type_field="model_type", object_id_field="model_id")

    class Meta:
        db_table = "users"

    def data(self):
        return model_to_dict(self)

    def oAuthToken(self):
        return self.oauth_access_token.model.objects.last()

    def permissions(self):
        modelHasRole = self.model_has_role.first()
        if modelHasRole is not None:
            role = modelHasRole.role
            if role is not None:
                return role.has_permissions.all()
        return None

    def hasPermission(self, name):
        modelHasRole = self.model_has_role.first()
        if modelHasRole is not None:
            role = modelHasRole.role
            if role is not None:
                permission = role.has_permissions.filter(**{"name": name, "guard_name": "backoffice"})
                if len(list(permission)) != 0:
                    return True
        return False
