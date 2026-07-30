from django.urls import path

from .views import (
    CartAPIView,
    CartAddItemAPIView,
    UpdateCartItemAPIView,
    DeleteCartItemAPIView,
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
    path(
        "items/<uuid:item_id>/update/",
        UpdateCartItemAPIView.as_view(),
        name="cart-update-item",
    ),
    path(
        "items/<uuid:item_id>/delete/",
        DeleteCartItemAPIView.as_view(),
        name="cart-delete-item",
    ),
]
