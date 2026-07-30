from rest_framework.generics import ListAPIView
from rest_framework.throttling import ScopedRateThrottle

from store.repositories import CategoryRepository
from store.api.v1.serializers import CategorySerializer, CategoryDetailSerializer


class CategoryListAPIView(ListAPIView):
    """
    API endpoint for categories.
    """

    http_method_names = ["get"]

    serializer_class = CategorySerializer

    throttle_scope = "anon"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore

        return CategoryRepository.get_all()


class CategoryDetailAPIView(ListAPIView):
    """
    API endpoint for categories detail.
    """

    http_method_names = ["get"]

    serializer_class = CategoryDetailSerializer

    throttle_scope = "anon"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore

        return CategoryRepository.get_with_products()
