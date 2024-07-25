import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict


class File(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=255, unique=True)
    file_name = models.CharField(max_length=255, db_collation="utf8mb4_unicode_ci")
    mime_type = models.CharField(max_length=255, db_index=True)
    collection_name = models.CharField(max_length=255, db_index=True)
    conversion = models.TextField(null=True, default=None)
    size_bytes = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "files"

    def data(self):
        return model_to_dict(self)
