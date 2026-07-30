from django.db.models import QuerySet, Prefetch

from cart.models import (
    CartModel,
    CartItemModel,
)


class CartRepository:
    """Database operations for cart."""

    @staticmethod
    def get_by_user(user) -> CartModel | None:

        return (
            CartModel.objects.filter(user=user)
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=CartItemModel.objects.select_related(
                        "variant",
                        "variant__product",
                    )
                    .prefetch_related(
                        "variant__attribute_values__attribute",
                        "variant__images",
                    )
                    .order_by("-added_at"),
                )
            )
            .first()
        )

    @staticmethod
    def get_by_session_key(session_key: str) -> CartModel | None:

        return (
            CartModel.objects.filter(session_key=session_key)
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=CartItemModel.objects.select_related(
                        "variant",
                        "variant__product",
                    )
                    .prefetch_related(
                        "variant__attribute_values__attribute",
                        "variant__images",
                    )
                    .order_by("-added_at"),
                )
            )
            .first()
        )

    @staticmethod
    def create(*, user=None, session_key=None):

        return CartModel.objects.create(
            user=user,
            # session_key=session_key,
        )

    @staticmethod
    def get_item(item_id):
        return CartItemModel.objects.get(id=item_id)

    @staticmethod
    def get_item_variant(*, cart, variant):

        return (
            CartItemModel.objects.select_related(
                "variant",
                "variant__product",
            )
            .filter(
                cart=cart,
                variant=variant,
            )
            .first()
        )

    @staticmethod
    def create_item(*, cart, variant, quantity):

        return CartItemModel.objects.create(
            cart=cart,
            variant=variant,
            quantity=quantity,
        )

    @staticmethod
    def update_item_quantity(item, quantity):

        item.quantity = quantity

        item.save(
            update_fields=[
                "quantity",
                "updated_at",
            ]
        )

        return item

    @staticmethod
    def delete_item(item):

        item.delete()
