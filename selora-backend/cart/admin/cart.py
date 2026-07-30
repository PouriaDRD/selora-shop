from django.contrib import admin
from django.db.models import (
    Count,
    Sum,
    F,
    Case,
    When,
    DecimalField,
    ExpressionWrapper,
)

from cart.models import CartModel

from .cart_item import CartItemInline


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "session_key_display",
        "user",
        "items_count",
        "total_price_display",
        "updated_at",
        "created_at",
    )

    list_select_related = ("user",)

    search_fields = (
        "session_key",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__phone_number",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "id",
        "session_key",
        "items_count",
        "total_price_display",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("user",)

    ordering = ("-updated_at",)

    list_per_page = 50

    date_hierarchy = "created_at"

    inlines = [
        CartItemInline,
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "user",
                    "session_key",
                )
            },
        ),
        (
            "Summary",
            {
                "fields": (
                    "items_count",
                    "total_price_display",
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
        queryset = super().get_queryset(request)

        return queryset.annotate(
            cart_items_count=Count(
                "items",
                distinct=True,
            ),
            cart_total_price=Sum(
                ExpressionWrapper(
                    F("items__quantity")
                    * Case(
                        When(
                            items__variant__price_override__isnull=False,
                            then=F("items__variant__price_override"),
                        ),
                        default=F("items__variant__product__base_price"),
                        output_field=DecimalField(
                            max_digits=12,
                            decimal_places=2,
                        ),
                    ),
                    output_field=DecimalField(
                        max_digits=12,
                        decimal_places=2,
                    ),
                )
            ),
        )

    @admin.display(description="Session Key")
    def session_key_display(self, obj: CartModel):
        return obj.session_key[:8]

    @admin.display(description="Items")
    def items_count(self, obj: CartModel):
        return obj.cart_items_count  # type: ignore

    @admin.display(description="Total Price")
    def total_price_display(self, obj: CartModel):
        return f"{obj.cart_total_price or 0:,.0f}"  # type: ignore
