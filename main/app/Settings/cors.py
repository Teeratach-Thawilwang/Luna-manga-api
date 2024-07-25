from .path import STORAGE_DIR, env

# SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
CORS_ALLOW_ALL_ORIGINS = True
if "*" in list(env("ALLOWED_HOSTS", default=["localhost"])):
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = list(env("ALLOWED_HOSTS", default=["localhost"]))

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
