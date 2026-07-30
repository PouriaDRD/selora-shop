import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from cart.services import CartService
from cart.api.v1.serializers import CartSerializer

logger = logging.getLogger("CartAPIView")


class CartAPIView(APIView):
    """
    API endpoint for retrieving cart details.
    """

    http_method_names = [
        "get",
    ]

    permission_classes = [
        AllowAny,
    ]

    throttle_scope = "anon"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def get(self, request: Request, *args, **kwargs):
        session_key = request.query_params.get("session_key", None)

        cart = CartService.get_or_create_cart(
            user=(request.user if request.user.is_authenticated else None),
            session_key=session_key,
        )

        serializer = CartSerializer(cart)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
