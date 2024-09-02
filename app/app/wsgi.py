"""
WSGI config for setting project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

import dotenv
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

dotenv.load_dotenv()

if "test" in sys.argv:
    os.environ.setdefault("APP_ENV", "test")
elif "qcluster" in sys.argv:
    os.environ.setdefault("APP_ENV", "worker")
else:
    os.environ.setdefault("APP_ENV", os.environ.get("APP_ENV"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

if settings.DEBUG:
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application()
