from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.models import model_to_dict


class Fileable(models.Model):
    file = models.ForeignKey("File", on_delete=models.CASCADE)
    model_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    model_id = models.PositiveIntegerField()
    model = GenericForeignKey("model_type", "model_id")

    class Meta:
        db_table = "fileables"

    def data(self):
        return model_to_dict(self)
