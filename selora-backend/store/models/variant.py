import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django_cleanup import cleanup
from django.core.validators import (
    FileExtensionValidator,
)

from .product import ProductModel
from .attribute import AttributeValueModel


class ProductVariantModel(models.Model):
    """
    A purchasable combination of attribute values for a product.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    sku = models.CharField(
        max_length=64,
        unique=True,
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    attribute_values = models.ManyToManyField(
        AttributeValueModel,
        related_name="variants",
        blank=True,
    )

    price_override = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

    @property
    def price(self):
        return (
            self.price_override
            if self.price_override is not None
            else self.product.base_price
        )

    @property
    def label(self):
        values = self.attribute_values.all()

        return " / ".join(value.value for value in values) if values else "Default"


def variant_image_upload_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1]
    return f"variants/" f"{instance.variant.id}/" f"{instance.id}.{ext}"


@cleanup.select
class VariantImageModel(models.Model):
    """
    An image for a variant.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    variant = models.ForeignKey(
        ProductVariantModel, on_delete=models.CASCADE, related_name="images"
    )

    image = models.ImageField(
        upload_to=variant_image_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )

    alt_text = models.CharField(max_length=200, blank=True)

    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = [
            "-is_main",
            "id",
        ]

        verbose_name = "Variant Image"
        verbose_name_plural = "Variant Images"

    def __str__(self):
        return f"Image variant for {self.variant.label} ({self.variant.product.name})"
