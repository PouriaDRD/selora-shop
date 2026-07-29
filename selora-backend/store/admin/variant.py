from django.contrib import admin

from store.models import ProductVariantModel, VariantImageModel


class VariantImageInline(admin.TabularInline):
    model = VariantImageModel
    extra = 1


@admin.register(ProductVariantModel)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "sku",
        "price",
        "stock",
        "is_active",
    ]

    list_filter = [
        "is_active",
        "product",
    ]

    search_fields = (
        "sku",
        "product__name",
    )

    filter_horizontal = [
        "attribute_values",
    ]

    inlines = [
        VariantImageInline,
    ]
