from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from config.settings.app_config import config

router = routers.DefaultRouter()

base_url = config.app.base_url
admin_url = config.app.admin_url

urlpatterns = [
    path(base_url, include(router.urls)),
    # Admin URL without base_url
    path(base_url + admin_url, admin.site.urls),
    # API documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # API routes
    path(base_url + "accounts/", include("accounts.api.urls")),
]


if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = "Selora Shop Admin"
admin.site.site_header = "Selora Shop Admin"
admin.site.site_title = "Selora Shop"
