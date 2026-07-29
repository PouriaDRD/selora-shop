from .base import *

DEBUG = True
ENABLE_DEBUG_TOOLBAR = True

# ---------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------
if USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "dev_db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config.database.db_name,
            "USER": config.database.db_user,
            "PASSWORD": config.database.db_password,
            "HOST": config.database.db_host,
            "PORT": config.database.db_port,
        }
    }

INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


# ---------------------------------------------------------------
# Static & Media Files
# ---------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# ---------------------------------------------------------------
# Django REST Framework Configuration
# ---------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": [
        "config.renderers.ApiRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "15/minute",
        "user": "40/minute",
        "login": "5/minute",
        "register": "5/minute",
        "refresh-token": "5/minute",
    },
    "EXCEPTION_HANDLER": "config.exception_handler.custom_exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Selora Shop API",
    "DESCRIPTION": "Selora Shop API Documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
