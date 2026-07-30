from rest_framework import serializers

from store.models import CategoryModel
from .product import ProductListSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = (
            "id",
            "name",
            "slug",
        )
        read_only_fields = ["__all__"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryModel
        fields = (
            "id",
            "name",
            "slug",
            "products",
        )
        read_only_fields = ["__all__"]
