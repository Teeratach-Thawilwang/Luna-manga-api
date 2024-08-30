from .path import env

CACHE = "test" if env("APP_ENV") == "test" else "default"
CACHES_AVAILABLE = {
    "test": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
    },
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:" + env("REDIS_PASSWORD") + "@" + env("REDIS_URL") + ":" + env("REDIS_PORT"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

CACHES = {
    "default": CACHES_AVAILABLE[CACHE],
}

CACHE_PAGE_IN_SECONDS = int(env("CACHE_PAGE_IN_SECONDS", default=60))
CACHE_PRESIGNED_URL_IN_SECONDS = int(env("CACHE_PRESIGNED_URL_IN_SECONDS", default=60))
