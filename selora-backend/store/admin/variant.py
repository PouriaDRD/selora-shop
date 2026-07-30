from django.contrib import admin

from store.models import (
    ProductVariantModel,
    VariantImageModel,
)


class VariantImageInline(admin.TabularInline):
    model = VariantImageModel
    extra = 1


@admin.register(ProductVariantModel)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = [
        "variant_name",
        "sku",
        "price",
        "stock",
        "is_active",
        "product",
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

    list_select_related = [
        "product",
    ]

    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        return queryset.prefetch_related("attribute_values__attribute")

    @admin.display(description="Variant")
    def variant_name(self, obj):

        values = obj.attribute_values.all()

        if not values:
            return "Default"

        return " / ".join(f"{v.attribute.name}: {v.value}" for v in values)
