from uuid import UUID
from typing import Any, Optional

from django.db.models import (
    QuerySet,
    Prefetch,
    Exists,
    OuterRef,
)

from store.models import (
    CategoryModel,
    ProductModel,
    ProductImageModel,
    ProductVariantModel,
)


class CategoryRepository:
    """
    Repository responsible only for database write operations.
    """

    @staticmethod
    def create(**kwargs: Any) -> CategoryModel:
        """Create a new category."""
        return CategoryModel.objects.create(**kwargs)

    @staticmethod
    def update(category: CategoryModel, **kwargs: Any) -> CategoryModel:
        """Update an existing category."""
        for field, value in kwargs.items():
            setattr(category, field, value)

        category.save()

        return category

    @staticmethod
    def delete(category: CategoryModel) -> None:
        """Delete an existing category."""
        category.delete()

    @staticmethod
    def bulk_create(categories: list[CategoryModel]) -> list[CategoryModel]:
        """Bulk create categories."""
        return CategoryModel.objects.bulk_create(categories)

    @staticmethod
    def get_by_id(category_id: str | UUID) -> CategoryModel:
        """Get category by id."""
        return CategoryModel.objects.get(id=category_id)

    @staticmethod
    def get_by_name(name: str) -> Optional[CategoryModel]:
        """Get category by name."""
        try:
            return CategoryModel.objects.get(name=name)
        except CategoryModel.DoesNotExist:
            return None

    @staticmethod
    def get_by_slug(slug: str) -> Optional[CategoryModel]:
        """Get category by slug."""
        try:
            return CategoryModel.objects.get(slug=slug)
        except CategoryModel.DoesNotExist:

            return None

    @staticmethod
    def get_all() -> QuerySet[CategoryModel]:
        """Get all categories."""
        return CategoryModel.objects.all()

    @staticmethod
    def search_by_name(query: str) -> QuerySet[CategoryModel]:
        """Search categories by name."""
        return CategoryModel.objects.filter(name__icontains=query)

    @staticmethod
    def get_with_products() -> QuerySet[CategoryModel]:
        """Get all categories with their products prefetched."""

        has_stock = ProductVariantModel.objects.filter(
            product=OuterRef("pk"),
            is_active=True,
            stock__gt=0,
        )

        products = (
            ProductModel.objects.filter(is_active=True)
            .annotate(has_stock=Exists(has_stock))
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImageModel.objects.filter(is_main=True),
                    to_attr="prefetched_main_images",
                )
            )
        )

        return CategoryModel.objects.prefetch_related(
            Prefetch("products", queryset=products)
        )
