from django.db import transaction
from django.core.exceptions import ValidationError

from cart.models import CartModel

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
    def get_or_create_cart(
        *,
        user=None,
        session_key=None,
    ):

        cart = None

        if user:
            cart = CartRepository.get_by_user(user)

        if not cart and session_key:
            cart = CartRepository.get_by_session_key(session_key)

        if not cart:
            cart = CartRepository.create(
                user=user,
            )

            cart = CartRepository.get_by_user(user)

        return cart

    @staticmethod
    @transaction.atomic
    def add_item(
        *,
        cart: CartModel,
        variant: ProductVariantModel,
        quantity: int,
    ):

        if not variant.is_active:
            raise ValidationError("The variant is not active.")

        if variant.stock < quantity:
            raise ValidationError("The variant is out of stock.")

        item = CartRepository.get_item(
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
    def update_quantity(
        *,
        item,
        quantity: int,
    ):

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
    def remove_item(item):

        return CartRepository.delete_item(item)
