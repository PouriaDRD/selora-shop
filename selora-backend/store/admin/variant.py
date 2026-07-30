from django.contrib import admin

from store.models import (
    ProductVariantModel,
    VariantImageModel,
    AttributeValueModel,
)

from store.forms import ProductVariantAdminForm


class VariantImageInline(admin.TabularInline):
    model = VariantImageModel

    extra = 0

    fields = (
        "image",
        "alt_text",
        "is_main",
    )


@admin.register(ProductVariantModel)
class ProductVariantAdmin(admin.ModelAdmin):

    form = ProductVariantAdminForm

    list_display = (
        "variant_name",
        "sku",
        "product",
        "price_display",
        "stock",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "product",
        "created_at",
    )

    search_fields = (
        "sku",
        "product__name",
        "attribute_values__value",
    )

    filter_horizontal = ("attribute_values",)

    list_select_related = ("product",)

    autocomplete_fields = ("product",)

    inlines = (VariantImageInline,)

    readonly_fields = (
        "created_at",
        "updated_at",
        "label_display",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "product",
                    "sku",
                    "attribute_values",
                    "label_display",
                )
            },
        ),
        (
            "Pricing & Stock",
            {
                "fields": (
                    "price_override",
                    "stock",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "product",
            )
            .prefetch_related(
                "attribute_values__attribute",
            )
        )

    def formfield_for_manytomany(
        self,
        db_field,
        request,
        **kwargs,
    ):

        if db_field.name == "attribute_values":

            kwargs["queryset"] = AttributeValueModel.objects.select_related(
                "attribute",
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
    def variant_name(
        self,
        obj: ProductVariantModel,
    ):
        return obj.label

    @admin.display(description="Price")
    def price_display(
        self,
        obj: ProductVariantModel,
    ):
        return f"{obj.price:,.0f}"

    @admin.display(description="Combination")
    def label_display(
        self,
        obj: ProductVariantModel,
    ):
        return obj.label
