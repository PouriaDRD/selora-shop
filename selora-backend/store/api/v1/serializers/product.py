from rest_framework import serializers

from store.models import (
    ProductModel,
    ProductImageModel,
    ProductVariantModel,
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = (
            "id",
            "image",
            "alt_text",
            "is_main",
        )


class ProductVariantShortSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField()
    label = serializers.ReadOnlyField()

    class Meta:
        model = ProductVariantModel
        fields = (
            "id",
            "sku",
            "label",
            "price",
            "stock",
            "is_active",
        )


class ProductListSerializer(serializers.ModelSerializer):

    main_image = serializers.SerializerMethodField()

    in_stock = serializers.BooleanField(source="has_stock", read_only=True)

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
        )

    def get_main_image(self, obj):

        images = getattr(obj, "main_image_list", [])

        if not images:
            return None

        return ProductImageSerializer(images[0], context=self.context).data


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    variants = ProductVariantShortSerializer(
        many=True,
        read_only=True,
    )

    in_stock = serializers.ReadOnlyField()

    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "category",
            "base_price",
            "min_price",
            "max_price",
            "in_stock",
            "images",
            "variants",
            "created_at",
        )

    def get_min_price(self, obj):
        return obj.price_range[0]

    def get_max_price(self, obj):
        return obj.price_range[1]
