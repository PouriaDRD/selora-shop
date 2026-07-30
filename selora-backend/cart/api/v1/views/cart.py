import logging

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from cart.services import CartService
from cart.api.v1.serializers import CartSerializer

from config.swagger import (
    THROTTLE_RESPONSE,
    SERVER_ERROR_RESPONSE,
)

logger = logging.getLogger("CartAPIView")


@extend_schema(
    tags=["Cart"],
    summary="Retrieve cart details",
    description="""
Retrieve current shopping cart information.

Returns:
- Cart details.
- Cart items.
- Total item count.
- Total cart price.

Features:
- Supports guest users with session_key.
- Supports authenticated users.
- Protected by anonymous rate limiting.

Possible errors:
- Too many requests.
- Server errors.
""",
    responses={
        200: OpenApiResponse(
            response=CartSerializer,
            description="Cart retrieved successfully.",
        ),
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
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

    def get(
        self,
        request: Request,
        *args,
        **kwargs,
    ):

        session_key = request.query_params.get(
            "session_key",
        )

        cart = CartService.get_or_create_cart(
            user=(request.user if request.user.is_authenticated else None),
            session_key=session_key,
        )

        serializer = CartSerializer(cart)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
