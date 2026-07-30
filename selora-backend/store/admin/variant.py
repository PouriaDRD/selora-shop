from django.contrib import admin

from store.models import (
    ProductVariantModel,
    VariantImageModel,
    AttributeValueModel,
)


class VariantImageInline(admin.TabularInline):
    model = VariantImageModel
    extra = 0


@admin.register(ProductVariantModel)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "variant_name",
        "sku",
        "price",
        "stock",
        "is_active",
        "product",
    )

    list_filter = (
        "is_active",
        "product",
    )

    search_fields = (
        "sku",
        "product__name",
    )

    filter_horizontal = ("attribute_values",)

    list_select_related = ("product",)

    inlines = (VariantImageInline,)

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related("product")
            .prefetch_related(
                "attribute_values__attribute",
            )
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if db_field.name == "attribute_values":
            kwargs["queryset"] = AttributeValueModel.objects.select_related(
                "attribute"
            ).order_by(
                "attribute__name",
                "value",
            )

        return super().formfield_for_manytomany(
            db_field,
            request,
            **kwargs,
        )

    @admin.display(description="Variant")
    def variant_name(self, obj):

        return obj.label
