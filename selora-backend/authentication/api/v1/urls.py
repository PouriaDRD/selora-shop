from django.urls import path

from .views import LoginAPIView, TokenRefreshAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="auth_login"),
    path("login/refresh/", TokenRefreshAPIView.as_view(), name="auth_refresh"),
]
