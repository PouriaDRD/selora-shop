import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from store.models import ProductVariantModel
from cart.api.v1.serializers import (
    CartAddItemSerializer,
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

        cart = CartService.get_or_create_cart(
            user=(request.user if request.user.is_authenticated else None),
            session_key=request.session.session_key,
        )

        item = CartService.add_item(
            cart=cart,
            variant=variant,
            quantity=serializer.validated_data["quantity"],  # type: ignore
        )

        return Response(
            data=item.id,
            status=status.HTTP_200_OK,
        )
