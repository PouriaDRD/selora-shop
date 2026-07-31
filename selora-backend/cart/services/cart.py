from django.db import transaction
from django.core.exceptions import ValidationError

from cart.models import CartModel, CartItemModel

from cart.repositories import (
    CartRepository,
)

from store.models import ProductVariantModel


class CartService:
    """
    Business logic for cart.
    """

    @staticmethod
    @transaction.atomic
    def get_or_create_cart(*, user=None, session_key=None):

        cart = None

        if user:
            cart = CartRepository.get_by_user(user)

        if not cart and session_key:
            cart = CartRepository.get_by_session_key(session_key)

        if not cart and user:
            cart = CartRepository.create(
                user=user,
                # session_key=session_key,
            )

            cart = CartRepository.get_by_user(user)

        # attach user to cart
        if user and not cart.user:  # type: ignore
            cart.user = user  # type: ignore
            cart.save()  # type: ignore

        if not cart and not user and not session_key:
            cart = CartRepository.create()

        return cart

    @staticmethod
    @transaction.atomic
    def add_item(*, cart: CartModel, variant: ProductVariantModel, quantity: int):

        if not variant.is_active:
            raise ValidationError("The variant is not active.")

        if variant.stock < quantity:
            raise ValidationError("The variant is out of stock.")

        item = CartRepository.get_item_variant(
            cart=cart,
            variant=variant,
        )

        if item:

            new_quantity = item.quantity + quantity

            if variant.stock < new_quantity:
                raise ValidationError("The variant is out of stock.")

            return CartRepository.update_item_quantity(
                item,
                new_quantity,
            )

        return CartRepository.create_item(
            cart=cart,
            variant=variant,
            quantity=quantity,
        )

    @staticmethod
    @transaction.atomic
    def update_quantity(*, item_id: str, quantity: int):
        item = CartRepository.get_item(item_id=item_id)

        if quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")

        if item.variant.stock < quantity:
            raise ValidationError("The variant is out of stock.")

        return CartRepository.update_item_quantity(
            item,
            quantity,
        )

    @staticmethod
    @transaction.atomic
    def remove_item(item_id: str):
        item = CartRepository.get_item(item_id=item_id)

        return CartRepository.delete_item(item)

    @staticmethod
    @transaction.atomic
    def merge_guest_cart(*, user, session_key: str | None = None):

        guest_cart = (
            CartModel.objects.filter(
                session_key=session_key,
                user__isnull=True,
            )
            .prefetch_related(
                "items",
            )
            .first()
        )

        if not guest_cart:
            return None

        user_cart = CartModel.objects.filter(
            user=user,
        ).first()

        if not user_cart:
            user_cart = CartModel.objects.create(
                user=user,
            )

        for guest_item in guest_cart.items.all():  # type: ignore

            existing = CartItemModel.objects.filter(
                cart=user_cart,
                variant=guest_item.variant,
            ).first()

            if existing:

                existing.quantity += guest_item.quantity

                existing.save(
                    update_fields=[
                        "quantity",
                        "updated_at",
                    ]
                )

            else:

                CartItemModel.objects.create(
                    cart=user_cart,
                    variant=guest_item.variant,
                    quantity=guest_item.quantity,
                )

        guest_cart.delete()

        return user_cart
