from rest_framework import serializers
from store.models import (
    VariantImageModel,
    ProductVariantModel,
)


class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImageModel
        fields = (
            "id",
            "image",
            "alt_text",
            "is_main",
        )


class VariantSerializer(serializers.ModelSerializer):
    images = VariantImageSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariantModel
        fields = (
            "id",
            "sku",
            "label",
            "price",
            "stock",
            "is_active",
            "images",
        )

    def get_price(self, obj):
        if obj.price_override is not None:
            return obj.price_override
        return obj.product.base_price

    def get_label(self, obj):
        values = obj.attribute_values.all()
        if not values:
            return "Default"
        return " / ".join(v.value for v in values)
