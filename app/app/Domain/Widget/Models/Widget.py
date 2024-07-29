from django.db import models
from django.forms.models import model_to_dict


class Widget(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, db_collation="utf8mb4_unicode_ci")
    title = models.CharField(max_length=150, db_collation="utf8mb4_unicode_ci")
    type = models.CharField(max_length=150)
    status = models.CharField(max_length=30, default="inactive")
    updated_by = models.ForeignKey("User", on_delete=models.SET_DEFAULT, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "widgets"

    def data(self):
        return model_to_dict(self)
