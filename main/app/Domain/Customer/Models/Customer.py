from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict


class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=150, db_index=True)
    password = models.CharField(max_length=150)
    nick_name = models.CharField(max_length=150, null=True, default=None, db_collation="utf8mb4_unicode_ci")
    first_name = models.CharField(max_length=150, db_collation="utf8mb4_unicode_ci")
    last_name = models.CharField(max_length=150, db_collation="utf8mb4_unicode_ci")
    phone_number = models.CharField(max_length=20, null=True, default=None)
    status = models.CharField(max_length=30, default="inactive")
    last_login = models.DateTimeField(null=True, default=None)
    email_verified_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    customer_group = models.ForeignKey("CustomerGroup", on_delete=models.SET_DEFAULT, default=1)
    oauth_access_token = GenericRelation("OAuthAccessToken", content_type_field="model_type", object_id_field="model_id")
    model_has_role = GenericRelation("ModelHasRole", content_type_field="model_type", object_id_field="model_id")
    fileable = GenericRelation("Fileable", content_type_field="model_type", object_id_field="model_id")

    class Meta:
        db_table = "customers"

    def data(self):
        return model_to_dict(self)

    def oAuthToken(self):
        return self.oauth_access_token.model.objects.last()

    def group(self):
        return self.customer_group

    def permissions(self):
        modelHasRole = self.model_has_role.first()
        if modelHasRole is not None:
            role = modelHasRole.role
            if role is not None:
                return role.has_permissions.all()
        return None
