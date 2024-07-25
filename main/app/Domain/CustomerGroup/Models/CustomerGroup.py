from django.db import models
from django.forms.models import model_to_dict


class CustomerGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150, db_collation="utf8mb4_unicode_ci")
    status = models.CharField(max_length=30, default="inactive")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "customer_groups"

    def data(self):
        return model_to_dict(self)

    def totalCustomers(self):
        return self.customer_set.count()
