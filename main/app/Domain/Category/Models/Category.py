from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, db_collation="utf8mb4_unicode_ci")
    type = models.CharField(max_length=150)
    status = models.CharField(max_length=30, default="inactive")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fileable = GenericRelation("Fileable", content_type_field="model_type", object_id_field="model_id")

    class Meta:
        db_table = "categories"
        constraints = [models.UniqueConstraint(fields=["name", "type"], name="unique_name_type")]

    def data(self):
        return model_to_dict(self)
