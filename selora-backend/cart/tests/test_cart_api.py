from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import CartItemModel

from .factories import (
    create_variant,
    create_cart,
)


class CartAPITest(APITestCase):

    def setUp(self):
        self.session_key = "test-session-key"

        self.variant = create_variant()

        self.cart = create_cart(
            session_key=self.session_key,
        )

    def test_get_cart(self):
        response = self.client.get(
            "/api/v1/cart/",
            {
                "session_key": self.session_key,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "items",
            response.data,  # type: ignore
        )

        self.assertEqual(
            response.data["items_count"],  # type: ignore
            0,
        )

    def test_add_item_to_cart(self):

        response = self.client.post(
            "/api/v1/cart/items/add/",
            {
                "cart_session_key": self.session_key,
                "variant_id": str(self.variant.id),
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["quantity"],  # type: ignore
            2,
        )

        self.assertTrue(
            CartItemModel.objects.filter(
                cart=self.cart,
                variant=self.variant,
            ).exists()
        )

    def test_update_cart_item_quantity(self):

        item = CartItemModel.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=1,
        )

        response = self.client.patch(
            f"/api/v1/cart/items/{item.id}/update/",
            {
                "quantity": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        item.refresh_from_db()

        self.assertEqual(
            item.quantity,
            5,
        )

    def test_delete_cart_item(self):

        item = CartItemModel.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=1,
        )

        response = self.client.delete(
            f"/api/v1/cart/items/{item.id}/delete/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            CartItemModel.objects.filter(
                id=item.id,
            ).exists()
        )

    def test_cannot_add_inactive_variant(self):

        inactive_variant = create_variant(
            is_active=False,
        )

        response = self.client.post(
            "/api/v1/cart/items/add/",
            {
                "cart_session_key": self.session_key,
                "variant_id": str(inactive_variant.id),
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cannot_add_more_than_stock(self):

        variant = create_variant(
            stock=2,
        )

        response = self.client.post(
            "/api/v1/cart/items/add/",
            {
                "cart_session_key": self.session_key,
                "variant_id": str(variant.id),
                "quantity": 10,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
