from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict


class Banner(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, db_collation="utf8mb4_unicode_ci")
    title = models.CharField(max_length=300, db_collation="utf8mb4_unicode_ci")
    type = models.CharField(max_length=150)
    link = models.CharField(max_length=300, db_collation="utf8mb4_unicode_ci")
    status = models.CharField(max_length=30, default="inactive")
    model_id = models.IntegerField(null=True, default=None)  # direct to story or chapter
    updated_by = models.ForeignKey("User", on_delete=models.SET_DEFAULT, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fileable = GenericRelation("Fileable", content_type_field="model_type", object_id_field="model_id")

    class Meta:
        db_table = "banners"

    def data(self):
        return model_to_dict(self)
