from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.models import model_to_dict


class OAuthAccessToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    model_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, default=None)
    model_id = models.PositiveIntegerField(null=True, default=None)
    model = GenericForeignKey("model_type", "model_id")

    access_token = models.TextField(max_length=500, unique=True)
    refresh_token = models.TextField(max_length=500, unique=True)
    scopes = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, default=None)

    client = models.ForeignKey("OAuthClient", on_delete=models.CASCADE)

    class Meta:
        db_table = "oauth_access_tokens"

    def data(self):
        return model_to_dict(self)

    def owner(self):
        return self.model
