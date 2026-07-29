from django.contrib import admin

from store.models import ProductModel, ProductImageModel, ProductVariantModel


class ProductImageInline(admin.TabularInline):
    model = ProductImageModel
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariantModel
    extra = 1
    filter_horizontal = ("attribute_values",)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "base_price",
        "is_active",
        "in_stock",
    ]

    list_filter = [
        "is_active",
        "category",
    ]

    search_fields = [
        "name",
        "description",
    ]

    prepopulated_fields = {
        "slug": ("name",),
    }

    inlines = [ProductImageInline, ProductVariantInline]

    @admin.display(boolean=True)
    def in_stock(self, obj):
        return obj.in_stock
