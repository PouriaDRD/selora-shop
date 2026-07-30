import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_cleanup import cleanup
from django.core.validators import (
    FileExtensionValidator,
)

from .category import CategoryModel


class ProductModel(models.Model):
    """
    A product is a unique combination of a name and a category.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )

    description = models.TextField(blank=True)

    base_price = models.PositiveBigIntegerField(
        default=0,
        help_text="Price used when a variant does not override it.",
    )

    is_active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    @property
    def main_image(self):
        img = self.images.filter(is_main=True).first() or self.images.first()  # type: ignore
        return img

    @property
    def in_stock(self):
        return self.variants.filter(is_active=True, stock__gt=0).exists()  # type: ignore

    @property
    def price_range(self):
        """Return (min_price, max_price) across active variants, falling back to base_price."""
        prices = [v.price for v in self.variants.filter(is_active=True)]  # type: ignore
        if not prices:
            return self.base_price, self.base_price
        return min(prices), max(prices)


def product_image_upload_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1]
    return f"products/" f"{instance.product.id}/" f"{instance.id}.{ext}"


@cleanup.select
class ProductImageModel(models.Model):
    """
    An image for a product.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name="images"
    )

    image = models.ImageField(
        upload_to=product_image_upload_path,
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

        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"Image for {self.product.name}"
