from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict


class Story(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey("Customer", on_delete=models.SET_DEFAULT, null=True, default=None)
    slug = models.CharField(db_index=True, unique=True, max_length=200, db_collation="utf8mb4_unicode_ci")
    name = models.CharField(unique=True, max_length=150, db_collation="utf8mb4_unicode_ci")
    author_name = models.CharField(max_length=150, db_collation="utf8mb4_unicode_ci", null=True, default=None)
    description = models.TextField(db_collation="utf8mb4_unicode_ci")
    type = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    categories = models.ManyToManyField("Category")
    fileable = GenericRelation("Fileable", content_type_field="model_type", object_id_field="model_id")
    customerReport = GenericRelation("CustomerReport", content_type_field="model_type", object_id_field="model_id")

    class Meta:
        db_table = "stories"

    def data(self):
        return model_to_dict(self)
