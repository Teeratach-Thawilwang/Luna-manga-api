from django.db import models
from django.forms.models import model_to_dict


class WidgetSequence(models.Model):
    id = models.BigAutoField(primary_key=True)
    widget = models.ForeignKey("Widget", on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "widgets_sequence"

    def data(self):
        return model_to_dict(self)
