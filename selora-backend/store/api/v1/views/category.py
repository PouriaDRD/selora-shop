from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from rest_framework.generics import ListAPIView
from rest_framework.throttling import ScopedRateThrottle

from store.repositories import CategoryRepository
from store.api.v1.serializers import (
    CategorySerializer,
    CategoryDetailSerializer,
)

from config.swagger import (
    THROTTLE_RESPONSE,
    SERVER_ERROR_RESPONSE,
)


@extend_schema(
    tags=["Store"],
    summary="List categories",
    description="""
Retrieve all available product categories.

This endpoint returns a paginated list of categories.

Features:
- Returns active categories.
- Supports public access.
- Protected by anonymous rate limiting.

Possible errors:
- Too many requests
- Server errors
""",
    responses={
        200: OpenApiResponse(
            response=CategorySerializer(many=True),
            description="Categories retrieved successfully.",
        ),
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class CategoryListAPIView(ListAPIView):
    """
    API endpoint for retrieving product categories.
    """

    http_method_names = [
        "get",
    ]

    serializer_class = CategorySerializer

    throttle_scope = "anon"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def get_queryset(self):  # type: ignore

        return CategoryRepository.get_all()


@extend_schema(
    tags=["Store"],
    summary="Retrieve category details",
    description="""
Retrieve detailed information about a specific category.

The response includes:
- Category information.
- Related products belonging to the category.

Possible errors:
- Category not found.
- Too many requests.
- Server errors.
""",
    responses={
        200: OpenApiResponse(
            response=CategoryDetailSerializer,
            description="Category details retrieved successfully.",
        ),
        404: OpenApiResponse(
            description="Category not found.",
        ),
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class CategoryDetailAPIView(ListAPIView):
    """
    API endpoint for retrieving category details.
    """

    http_method_names = [
        "get",
    ]

    serializer_class = CategoryDetailSerializer

    throttle_scope = "anon"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def get_queryset(self):  # type: ignore

        return CategoryRepository.get_with_products()
