import uuid

from django.core.validators import MinValueValidator
from django.db import models

from store.models import ProductVariantModel

from .cart import CartModel


class CartItemModel(models.Model):
    """
    An item in a cart.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    cart = models.ForeignKey(
        CartModel,
        related_name="items",
        on_delete=models.CASCADE,
        db_index=True,
    )

    variant = models.ForeignKey(
        ProductVariantModel,
        related_name="cart_items",
        on_delete=models.CASCADE,
        db_index=True,
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-added_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "variant"],
                name="unique_cart_variant",
            )
        ]

        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["variant"]),
            models.Index(fields=["added_at"]),
        ]

        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.quantity} × {self.variant}"

    @property
    def subtotal(self):
        return self.variant.price * self.quantity
