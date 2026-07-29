from django.urls import path

from .views import (
    LoginAPIView,
    RegisterAPIView,
    TokenRefreshAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="auth_login"),
    path("register/", RegisterAPIView.as_view(), name="auth_register"),
    path("login/refresh/", TokenRefreshAPIView.as_view(), name="auth_refresh"),
]
