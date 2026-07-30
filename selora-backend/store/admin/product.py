from django.contrib import admin
from django.db.models import Exists, OuterRef

from store.models import (
    ProductModel,
    ProductImageModel,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImageModel
    extra = 1


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "category",
        "base_price",
        "final_price",
        "stock_status",
        "is_active",
        "created_at",
    ]

    prepopulated_fields = {
        "slug": ("name",),
    }

    list_filter = [
        "is_active",
        "category",
    ]

    search_fields = [
        "name",
        "slug",
    ]

    inlines = [
        ProductImageInline,
    ]

    list_select_related = [
        "category",
    ]

    def get_queryset(self, request):

        has_stock = ProductModel.objects.filter(
            id=OuterRef("id"),
            variants__is_active=True,
            variants__stock__gt=0,
        )

        return (
            super()
            .get_queryset(request)
            .select_related(
                "category",
            )
            .annotate(has_stock=Exists(has_stock))
        )

    @admin.display(description="In Stock")
    def stock_status(self, obj):

        return "Yes" if obj.has_stock else "No"

    @admin.display(description="Price")
    def final_price(self, obj):

        return obj.base_price
