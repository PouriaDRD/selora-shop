from django.urls import path

from .views import (
    CartAPIView,
    CartAddItemAPIView,
)

urlpatterns = [
    path(
        "",
        CartAPIView.as_view(),
        name="cart",
    ),
    path(
        "items/add/",
        CartAddItemAPIView.as_view(),
        name="cart-add-item",
    ),
]
