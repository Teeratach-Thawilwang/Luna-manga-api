from django.db import models
from django.forms.models import model_to_dict


class WidgetBanner(models.Model):
    id = models.BigAutoField(primary_key=True)
    widget = models.ForeignKey("Widget", on_delete=models.CASCADE)
    banner = models.ForeignKey("Banner", on_delete=models.CASCADE)

    class Meta:
        db_table = "widgets_banners"

    def data(self):
        return model_to_dict(self)
