from django.contrib import admin

from cart.models import CartItemModel


class CartItemInline(admin.TabularInline):
    model = CartItemModel

    extra = 0

    autocomplete_fields = ("variant",)

    fields = (
        "variant",
        "quantity",
        "subtotal_display",
        "added_at",
        "updated_at",
    )

    readonly_fields = (
        "subtotal_display",
        "added_at",
        "updated_at",
    )

    ordering = ("-added_at",)

    show_change_link = True

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "variant",
                "variant__product",
            )
            .prefetch_related(
                "variant__attribute_values__attribute",
            )
        )

    @admin.display(description="Subtotal")
    def subtotal_display(self, obj):

        return f"{obj.subtotal:,.0f}"


@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "cart",
        "variant",
        "quantity",
        "subtotal_display",
        "added_at",
        "updated_at",
    )

    list_select_related = (
        "cart",
        "cart__user",
        "variant",
        "variant__product",
    )

    search_fields = (
        "id",
        "cart__session_key",
        "cart__user__username",
        "cart__user__phone_number",
        "variant__sku",
        "variant__product__name",
    )

    autocomplete_fields = (
        "cart",
        "variant",
    )

    readonly_fields = (
        "id",
        "subtotal_display",
        "added_at",
        "updated_at",
    )

    ordering = ("-added_at",)

    list_per_page = 50

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "cart",
                "cart__user",
                "variant",
                "variant__product",
            )
            .prefetch_related(
                "variant__attribute_values__attribute",
            )
        )

    @admin.display(description="Subtotal")
    def subtotal_display(self, obj):

        return f"{obj.subtotal:,.0f}"
