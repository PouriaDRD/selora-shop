import logging

from django.core.exceptions import ValidationError

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
from rest_framework.generics import GenericAPIView

from store.models import ProductVariantModel

from cart.services import CartService

from cart.api.v1.serializers import (
    CartItemSerializer,
    CartAddItemSerializer,
    CartUpdateItemSerializer,
)

from config.swagger import (
    THROTTLE_RESPONSE,
    SERVER_ERROR_RESPONSE,
)

logger = logging.getLogger("CartItemAPIView")


@extend_schema(
    tags=["Cart Items"],
    summary="Add item to cart",
    description="""
Add product variant to cart.

Features:
- Creates new cart item.
- Increases quantity if item already exists.
- Checks stock availability.
- Supports guest carts.

Possible errors:
- Invalid data.
- Variant inactive.
- Out of stock.
- Too many requests.
- Server errors.
""",
    request=CartAddItemSerializer,
    responses={
        200: OpenApiResponse(
            response=CartItemSerializer,
            description="Item added successfully.",
        ),
        400: OpenApiResponse(
            description="Invalid request.",
        ),
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class CartAddItemAPIView(APIView):

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

    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    ):

        serializer = CartAddItemSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        try:

            variant = ProductVariantModel.objects.select_related("product").get(
                id=serializer.validated_data["variant_id"]  # type: ignore
            )

            cart = CartService.get_or_create_cart(
                user=(request.user if request.user.is_authenticated else None),
                session_key=serializer.validated_data["cart_session_key"],  # type: ignore
            )

            item = CartService.add_item(
                cart=cart,  # type: ignore
                variant=variant,
                quantity=serializer.validated_data["quantity"],  # type: ignore
            )

            return Response(
                CartItemSerializer(item).data,
                status=status.HTTP_200_OK,
            )

        except ValidationError as exc:

            logger.warning(
                "Cart add validation error: %s",
                exc,
            )

            return Response(
                {
                    "detail": exc.messages[0],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(
    tags=["Cart Items"],
    summary="Update cart item quantity",
    description="""
Update quantity of existing cart item.

Possible errors:
- Invalid quantity.
- Not enough stock.
- Too many requests.
- Server errors.
""",
    request=CartUpdateItemSerializer,
    responses={
        200: OpenApiResponse(
            response=CartItemSerializer,
            description="Item updated successfully.",
        ),
        400: OpenApiResponse(
            description="Invalid quantity.",
        ),
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class UpdateCartItemAPIView(GenericAPIView):

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

    def patch(
        self,
        request: Request,
        *args,
        **kwargs,
    ):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        try:

            item = CartService.update_quantity(
                item_id=str(kwargs["item_id"]),
                quantity=serializer.validated_data["quantity"],
            )

            return Response(
                CartItemSerializer(item).data,
                status=status.HTTP_200_OK,
            )

        except ValidationError as exc:

            return Response(
                {
                    "detail": exc.messages[0],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(
    tags=["Cart Items"],
    summary="Delete cart item",
    description="""
Remove item from shopping cart.

Possible errors:
- Item not found.
- Too many requests.
- Server errors.
""",
    responses={
        200: OpenApiResponse(
            description="Item removed successfully.",
        ),
        400: OpenApiResponse(
            description="Unable to remove item.",
        ),
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class DeleteCartItemAPIView(GenericAPIView):

    permission_classes = [
        AllowAny,
    ]

    http_method_names = [
        "delete",
    ]

    throttle_scope = "anon"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def delete(
        self,
        request: Request,
        *args,
        **kwargs,
    ):

        try:

            CartService.remove_item(
                item_id=str(kwargs["item_id"]),
            )

            return Response(
                {
                    "message": "Cart item removed successfully.",
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as exc:

            return Response(
                {
                    "detail": exc.messages[0],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
