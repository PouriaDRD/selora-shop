from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/refresh/", TokenRefreshView.as_view(), name="auth_refresh"),
]
