import secrets
import uuid

from django.conf import settings
from django.db import models
from django.db.models import (
    F,
    Sum,
    DecimalField,
    ExpressionWrapper,
    Case,
    When,
)


class CartModel(models.Model):
    """
    One cart per anonymous session (or per logged-in user, if used later).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    session_key = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="carts",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]

        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def save(self, *args, **kwargs):
        if not self.session_key:
            self.session_key = secrets.token_urlsafe(32)

        super().save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return f"Cart ({self.user})"

        return f"Guest Cart ({self.session_key})"

    @property
    def total_items(self):
        return (
            self.items.aggregate(  # type: ignore
                total=Sum("quantity"),
            )["total"]
            or 0
        )

    @property
    def total_price(self):
        return (
            self.items.annotate(  # type: ignore
                final_price=Case(
                    When(
                        variant__price_override__isnull=False,
                        then=F("variant__price_override"),
                    ),
                    default=F("variant__product__base_price"),
                    output_field=DecimalField(
                        max_digits=12,
                        decimal_places=2,
                    ),
                )
            ).aggregate(
                total=Sum(
                    ExpressionWrapper(
                        F("quantity") * F("final_price"),
                        output_field=DecimalField(
                            max_digits=12,
                            decimal_places=2,
                        ),
                    )
                )
            )[
                "total"
            ]
            or 0
        )
