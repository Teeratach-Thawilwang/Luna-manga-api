from django.db import models
from django.forms.models import model_to_dict


class Bookmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    story = models.ForeignKey("Story", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bookmarks"

    def data(self):
        return model_to_dict(self)
