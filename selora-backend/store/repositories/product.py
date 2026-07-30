from uuid import UUID
from typing import Any, Optional

from django.db.models import (
    QuerySet,
    Prefetch,
    Exists,
    OuterRef,
    Min,
    Max,
    Q,
)

from store.models import (
    ProductModel,
    ProductImageModel,
    ProductVariantModel,
    AttributeValueModel,
    VariantImageModel,
)


class ProductRepository:
    """
    Repository responsible only for database write operations.
    """

    @staticmethod
    def create(**kwargs: Any) -> ProductModel:
        """Create a new Product."""
        return ProductModel.objects.create(**kwargs)

    @staticmethod
    def update(category: ProductModel, **kwargs: Any) -> ProductModel:
        """Update an existing Product."""
        for field, value in kwargs.items():
            setattr(category, field, value)

        category.save()

        return category

    @staticmethod
    def delete(category: ProductModel) -> None:
        """Delete an existing Product."""
        category.delete()

    @staticmethod
    def bulk_create(categories: list[ProductModel]) -> list[ProductModel]:
        """Bulk create products."""
        return ProductModel.objects.bulk_create(categories)

    @staticmethod
    def get_by_id(category_id: str | UUID) -> ProductModel:
        """Get product by id."""
        return ProductModel.objects.get(id=category_id)

    @staticmethod
    def get_by_name(name: str) -> Optional[ProductModel]:
        """Get product by name."""
        try:
            return ProductModel.objects.get(name=name)
        except ProductModel.DoesNotExist:
            return None

    @staticmethod
    def get_by_slug(slug: str) -> Optional[ProductModel]:
        """Get product by slug."""
        try:
            return ProductModel.objects.get(slug=slug)
        except ProductModel.DoesNotExist:

            return None

    @staticmethod
    def get_all() -> QuerySet[ProductModel]:
        """Get all products."""
        main_images = ProductImageModel.objects.filter(is_main=True)

        return ProductModel.objects.prefetch_related(
            Prefetch(
                "images",
                queryset=main_images,
                to_attr="prefetched_main_images",
            )
        ).order_by("-created_at")

    @staticmethod
    def search_by_name(query: str) -> QuerySet[ProductModel]:
        """Search products by name."""
        return ProductModel.objects.filter(name__icontains=query)

    @staticmethod
    def get_with_variants() -> QuerySet[ProductModel]:
        """Get all products with their variants prefetched."""

        has_stock = ProductVariantModel.objects.filter(
            product=OuterRef("pk"),
            is_active=True,
            stock__gt=0,
        )

        variant_queryset = ProductVariantModel.objects.filter(
            is_active=True
        ).prefetch_related(
            Prefetch("images", queryset=VariantImageModel.objects.all()),
            "attribute_values__attribute",
        )

        return (
            ProductModel.objects.filter(is_active=True)
            .select_related(
                "category",
            )
            .annotate(
                has_stock=Exists(has_stock),
                min_price=Min(
                    "variants__price_override", filter=Q(variants__is_active=True)
                ),
                max_price=Max(
                    "variants__price_override", filter=Q(variants__is_active=True)
                ),
            )
            .prefetch_related(
                "images",
                Prefetch(
                    "variants",
                    queryset=variant_queryset,
                ),
            )
        )
