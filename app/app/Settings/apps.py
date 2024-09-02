from .path import STORAGE_DIR, env

APP_URL = env("APP_URL")
SECRET_KEY = env("SECRET_KEY")
DEBUG = True if env("DEBUG") == "True" else False

CUSTOMER_ADMIN_EMAIL = env("CUSTOMER_ADMIN_EMAIL")
CUSTOMER_ADMIN_PASSWORD = env("CUSTOMER_ADMIN_PASSWORD")
SUPER_USER_ADMIN_EMAIL = env("SUPER_USER_ADMIN_EMAIL")
SUPER_USER_PASSWORD = env("SUPER_USER_PASSWORD")

ROOT_URLCONF = "app.Routes.urls"
ALLOWED_HOSTS = list(env("ALLOWED_HOSTS", default=["localhost"]))
WSGI_APPLICATION = "app.wsgi.application"
STATIC_URL = STORAGE_DIR + "static/"

INSTALLED_APPS = [
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    # "django.contrib.sessions",
    # "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_q",
    "app",
    "silk",
]

if env("APP_ENV") != "test":
    INSTALLED_APPS.append("corsheaders")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "app.Middlewares.ExceptionMiddleware.ExceptionMiddleware",
    "silk.middleware.SilkyMiddleware",
    "app.Middlewares.RequestParserMiddleware.RequestParserMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["/root/main/app/app/Templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

PASSWORD_HASHERS = [
    "app.Providers.HashProvider.HashProvider",
]
