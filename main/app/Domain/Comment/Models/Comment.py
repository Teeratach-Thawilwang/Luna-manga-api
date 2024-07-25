from django.db import models
from django.forms.models import model_to_dict


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    chapter = models.ForeignKey("Chapter", on_delete=models.CASCADE)
    text = models.TextField(db_collation="utf8mb4_unicode_ci")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"

    def data(self):
        return model_to_dict(self)
