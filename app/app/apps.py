import os

from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        from app.Schedules.Schedules import scheduler

        # Comment this section when intial database
        if os.environ.get("APP_ENV") in ["dev", "production"]:
            scheduler().handle()
