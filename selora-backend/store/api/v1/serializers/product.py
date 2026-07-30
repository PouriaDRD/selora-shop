from rest_framework import serializers

from store.models import (
    ProductModel,
    ProductImageModel,
    ProductVariantModel,
)
from .variant import VariantSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = (
            "id",
            "image",
            "alt_text",
            "is_main",
        )


class ProductListSerializer(serializers.ModelSerializer):

    main_image = serializers.SerializerMethodField()

    in_stock = serializers.BooleanField(
        source="has_stock",
        read_only=True,
    )

    class Meta:

        model = ProductModel

        fields = (
            "id",
            "name",
            "slug",
            "description",
            "base_price",
            "main_image",
            "in_stock",
            "created_at",
        )

    def get_main_image(self, obj):

        images = getattr(obj, "prefetched_main_images", [])

        if not images:
            return None

        return ProductImageSerializer(
            images[0],
            context=self.context,
        ).data


class ProductDetailSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    variants = VariantSerializer(
        many=True,
        read_only=True,
    )

    min_price = serializers.IntegerField(
        read_only=True,
    )

    max_price = serializers.IntegerField(
        read_only=True,
    )

    in_stock = serializers.BooleanField(
        source="has_stock",
        read_only=True,
    )

    class Meta:

        model = ProductModel

        fields = (
            "id",
            "name",
            "slug",
            "description",
            "base_price",
            "min_price",
            "max_price",
            "in_stock",
            "images",
            "variants",
            "created_at",
        )
