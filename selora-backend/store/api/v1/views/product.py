from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from config.swagger import (
    THROTTLE_RESPONSE,
    SERVER_ERROR_RESPONSE,
)

from store.repositories import ProductRepository
from store.api.v1.serializers import ProductDetailSerializer, ProductListSerializer


@extend_schema(
    tags=["Store"],
    summary="List products",
    description="""
Retrieve all available products.

This endpoint returns a paginated list of products.

Features:
- Returns active products.
- Supports public access.
- Protected by anonymous rate limiting.

Possible errors:
- Too many requests
- Server errors
""",
    responses={
        200: OpenApiResponse(
            response=ProductListSerializer(many=True),
            description="Products retrieved successfully.",
        ),
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class ProductListAPIView(ListAPIView):
    """
    API endpoint for retrieving product details.
    """

    http_method_names = [
        "get",
    ]

    serializer_class = ProductListSerializer

    throttle_scope = "anon"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def get_queryset(self):  # type: ignore

        return ProductRepository.get_all()


@extend_schema(
    tags=["Store"],
    summary="Retrieve product details",
    description="""
Retrieve detailed information about a specific product.

The response includes:
- Product information.
- Related variants belonging to the product.

Possible errors:
- Product not found.
- Too many requests.
- Server errors.
""",
    responses={
        200: OpenApiResponse(
            response=ProductDetailSerializer,
            description="Product details retrieved successfully.",
        ),
        404: OpenApiResponse(
            description="Product not found.",
        ),
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer

    lookup_field = "slug"

    http_method_names = [
        "get",
    ]

    throttle_scope = "anon"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def get_queryset(self):  # type: ignore

        return ProductRepository.get_with_variants()
