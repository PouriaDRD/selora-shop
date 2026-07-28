from .base import *
from .app_config import config

DEBUG = False
ENABLE_DEBUG_TOOLBAR = False

# ---------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------
if USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "prod_db.sqlite3",
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

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

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
    "DEFAULT_RENDERER_CLASSES": [
        # "rest_framework.renderers.JSONRenderer",
        "config.renderers.ApiRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
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
