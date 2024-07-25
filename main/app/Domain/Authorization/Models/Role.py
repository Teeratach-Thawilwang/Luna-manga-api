from django.db import models
from django.forms.models import model_to_dict


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    guard_name = models.CharField(max_length=255)
    name = models.CharField(unique=True, max_length=150, db_collation="utf8mb4_unicode_ci")
    description = models.CharField(max_length=255, db_collation="utf8mb4_unicode_ci")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_permissions = models.ManyToManyField("Permission")

    class Meta:
        db_table = "roles"

    def data(self):
        return model_to_dict(self)

    def permission(self):
        return self.has_permissions

    def permissions(self):
        return self.has_permissions.all()

    def modelHasRoles(self):
        return self.modelhasrole_set.all()
