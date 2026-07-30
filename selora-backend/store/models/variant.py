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
    A purchasable combination of attribute values for a product (e.g. Red / M).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # The SKU is a unique identifier for a product variant.
    # It is used to identify the product variant in the database.
    sku = models.CharField(max_length=64, unique=True)

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
        help_text="Leave blank to use the product's base price.",
    )

    is_active = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        options = ", ".join(str(v) for v in self.attribute_values.all())
        return f"{self.product.name} ({options or 'default'})"

    @property
    def price(self):
        return (
            self.price_override
            if self.price_override is not None
            else self.product.base_price
        )

    @property
    def label(self):
        """Human readable option label, e.g. 'Red / M'."""
        values = self.attribute_values.all().order_by("attribute__name")
        return " / ".join(v.value for v in values) if values else "Default"

    def clean(self):
        # Prevent two variants of the same product sharing the exact same
        # set of attribute values (enforced at the form/admin level too,
        # since M2M validation needs the instance to already be saved).
        if self.pk:
            sibling_ids = self.product.variants.exclude(pk=self.pk).values_list(  # type: ignore
                "id", flat=True
            )
            my_values = set(self.attribute_values.values_list("id", flat=True))
            for sibling_id in sibling_ids:
                sibling_values = set(
                    ProductVariantModel.objects.get(
                        pk=sibling_id
                    ).attribute_values.values_list("id", flat=True)
                )
                if sibling_values == my_values:
                    raise ValidationError(
                        "Another variant of this product already uses this exact "
                        "combination of options."
                    )


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
