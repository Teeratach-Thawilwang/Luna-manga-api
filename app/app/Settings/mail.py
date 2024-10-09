from .path import STORAGE_DIR, env

EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True if env("EMAIL_USE_TLS") == "True" else False
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
