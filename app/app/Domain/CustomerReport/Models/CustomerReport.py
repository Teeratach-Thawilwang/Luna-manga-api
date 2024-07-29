from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.models import model_to_dict


class CustomerReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.CharField(max_length=150)
    customer = models.ForeignKey("Customer", on_delete=models.SET_DEFAULT, null=True, default=None)
    is_accept = models.BooleanField(default=False)
    accept_by = models.ForeignKey("User", on_delete=models.SET_DEFAULT, null=True, default=None)
    model_id = models.PositiveIntegerField()
    model_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    message = models.CharField(max_length=100, null=True, default=None, db_collation="utf8mb4_unicode_ci")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    model = GenericForeignKey("model_type", "model_id")

    class Meta:
        db_table = "customer_reports"

    def data(self):
        return model_to_dict(self)
