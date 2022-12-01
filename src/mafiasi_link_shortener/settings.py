"""
Django settings for mafiasi_link_shortener project.

Generated by "django-admin startproject" using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import sentry_sdk
from environs import Env
from sentry_sdk.integrations.django import DjangoIntegration

env = Env()
env.read_env(env.path("SHORTLINK_ENV_FILE", default=".env"))

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = env.bool("SHORTLINK_DEBUG", default=False)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "simple_openid_connect.integrations.django",
    "corsheaders",
    "mafiasi_link_shortener.links",
    "mafiasi_link_shortener.api",
]

if DEBUG:
    INSTALLED_APPS.insert(1, "whitenoise.runserver_nostatic")
    INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(3, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "mafiasi_link_shortener.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "mafiasi_link_shortener.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": env.dj_db_url("SHORTLINK_DB")}

CACHES = {"default": env.dj_cache_url("SHORTLINK_CACHE", default="dummy://")}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_ROOT = BASE_DIR / "mafiasi_link_shortener" / "root_static"

LOGIN_REDIRECT_URL = "swagger-ui"
LOGIN_URL = "/auth/"

VERSION = "0.1.0"

CORS_URLS_REGEX = r"^/api/.*$"

APPEND_SLASH = True

STATIC_ROOT = BASE_DIR.parent / "static"

if DEBUG:
    WHITENOISE_AUTOREFRESH = True

INTERNAL_IPS = ["127.0.0.1", "::1"]

if not DEBUG:
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 63072000  # two years

if env.bool("SHORTLINK_TRUST_REVERSE_PROXY", default=False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SENTRY_DSN = env.str("SHORTLINK_SENTRY_DSN", default=None)
if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
    )

# openid authentication
OPENID_ISSUER = env.str(
    "SHORTLINK_OPENID_ISSUER", default="https://identity.mafiasi.de/auth/realms/mafiasi"
)
OPENID_SCOPE = "openid shortlinks"
OPENID_CLIENT_ID = env.str("SHORTLINK_OPENID_CLIENT_ID")
OPENID_CLIENT_SECRET = env.str("SHORTLINK_OPENID_CLIENT_SECRET")
OPENID_REDIRECT_URI = None

# rest framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "simple_openid_connect.integrations.djangorestframework.authentication.AccessTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "simple_openid_connect.integrations.djangorestframework.permissions.HasTokenScope",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

# openapi schema settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Mafiasi Link Shortener",
    "CONTACT": {
        "name": "Server-Ag",
        "email": "ag-server@informatik.uni-hamburg.de",
    },
    "VERSION": VERSION,
    "LICENSE": {
        "name": "MIT",
        "url": "https://github.com/fsinfuhh/mafiasi_link_shortener/blob/master/LICENSE",
    },
    "SCHEMA_PATH_PREFIX": r"/api/",
    "COMPONENT_SPLIT_PATCH": True,
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "SWAGGER_UI_OAUTH2_CONFIG": {
        "clientId": "dev-client",
        "clientSecret": "public-secret",
        "scopes": OPENID_SCOPE,
        "useBasicAuthenticationWithAccessCodeGrant": True,
    }
    if DEBUG
    else {
        "scopes": OPENID_SCOPE,
    },
}

# Configurable properties
SECRET_KEY = env.str("SHORTLINK_SECRET_KEY")
ALLOWED_HOSTS = env.list("SHORTLINK_ALLOWED_HOSTS")

LINK_SHORT_LENGTH = env.int("SHORTLINK_LINK_LENGTH", default=6)
