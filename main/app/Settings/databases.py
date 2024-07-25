from .path import STORAGE_DIR, env

DATABASE = "test" if env("APP_ENV") == "test" else "default"
DATABASES_AVAILABLE = {
    "test": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": STORAGE_DIR + "db.test.sqlite3",
    },
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    },
}
DATABASES = {
    "default": DATABASES_AVAILABLE[DATABASE],
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
