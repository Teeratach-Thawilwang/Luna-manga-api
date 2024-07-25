from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.models import model_to_dict


class ModelHasRole(models.Model):
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    model_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    model_id = models.PositiveIntegerField()
    model = GenericForeignKey("model_type", "model_id")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["role", "model_type", "model_id"], name="unique_model_has_role")]
        db_table = "model_has_roles"

    def data(self):
        return model_to_dict(self)
