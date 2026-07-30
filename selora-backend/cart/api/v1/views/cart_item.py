import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.generics import GenericAPIView

from store.models import ProductVariantModel
from cart.api.v1.serializers import (
    CartItemSerializer,
    CartAddItemSerializer,
    CartUpdateItemSerializer,
)


from cart.services import CartService

logger = logging.getLogger("CartAddItemAPIView")


class CartAddItemAPIView(APIView):
    """
    API endpoint for adding item to cart.
    """

    http_method_names = [
        "post",
    ]

    permission_classes = [
        AllowAny,
    ]

    throttle_scope = "anon"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def post(self, request: Request, *args, **kwargs):

        serializer = CartAddItemSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        variant = ProductVariantModel.objects.select_related("product").get(
            id=serializer.validated_data["variant_id"]  # type: ignore
        )

        session_key = serializer.validated_data["cart_session_key"]  # type: ignore

        cart = CartService.get_or_create_cart(
            user=(request.user if request.user.is_authenticated else None),
            session_key=session_key,
        )

        item = CartService.add_item(
            cart=cart,  # type: ignore
            variant=variant,
            quantity=serializer.validated_data["quantity"],  # type: ignore
        )

        return Response(
            data=CartItemSerializer(item).data,
            status=status.HTTP_200_OK,
        )


class UpdateCartItemAPIView(GenericAPIView):
    """
    API endpoint for updating item in cart.
    """

    serializer_class = CartUpdateItemSerializer

    http_method_names = [
        "patch",
    ]

    permission_classes = [
        AllowAny,
    ]

    throttle_scope = "anon"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def patch(self, request: Request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        item_id = str(kwargs.get("item_id"))
        quantity = int(serializer.validated_data["quantity"])

        item = CartService.update_quantity(item_id=item_id, quantity=quantity)

        return Response(data=CartItemSerializer(item).data, status=status.HTTP_200_OK)


class DeleteCartItemAPIView(GenericAPIView):

    def delete(self, request: Request, *args, **kwargs):
        item_id = str(kwargs.get("item_id"))
        CartService.remove_item(item_id=item_id)

        return Response(data=None, status=status.HTTP_200_OK)
