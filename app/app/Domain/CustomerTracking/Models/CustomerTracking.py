from django.db import models
from django.forms.models import model_to_dict


class CustomerTracking(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey("Customer", on_delete=models.SET_DEFAULT, null=True, default=None)
    token = models.ForeignKey("OAuthAccessToken", on_delete=models.SET_DEFAULT, null=True, default=None)
    request_url = models.CharField(max_length=150, null=True, default=None, db_collation="utf8mb4_unicode_ci")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "customer_tracking"

    def data(self):
        return model_to_dict(self)
