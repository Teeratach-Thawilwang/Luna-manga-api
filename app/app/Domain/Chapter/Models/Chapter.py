from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict


class Chapter(models.Model):
    id = models.BigAutoField(primary_key=True)
    story = models.ForeignKey("Story", on_delete=models.SET_DEFAULT, null=True, default=None)
    name = models.CharField(max_length=150, db_collation="utf8mb4_unicode_ci")
    chapter_number = models.PositiveIntegerField(default=0)
    text = models.TextField(db_collation="utf8mb4_unicode_ci", null=True, default=None)
    type = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    fileable = GenericRelation("Fileable", content_type_field="model_type", object_id_field="model_id")
    customerReport = GenericRelation("CustomerReport", content_type_field="model_type", object_id_field="model_id")

    class Meta:
        db_table = "chapters"

    def data(self):
        return model_to_dict(self)
