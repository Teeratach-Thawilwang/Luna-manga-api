from django.db import models
from django.forms.models import model_to_dict


class StoryReaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    story = models.ForeignKey("Story", on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stories_reaction"

    def data(self):
        return model_to_dict(self)
