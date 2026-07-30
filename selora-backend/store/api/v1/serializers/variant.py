from rest_framework import serializers
from store.models import (
    VariantImageModel,
    ProductVariantModel,
    AttributeValueModel,
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


class VariantAttributeSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(
        source="attribute.name",
        read_only=True,
    )

    class Meta:
        model = AttributeValueModel

        fields = (
            "id",
            "attribute",
            "value",
        )


class VariantSerializer(serializers.ModelSerializer):
    images = VariantImageSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    attributes = VariantAttributeSerializer(
        source="attribute_values",
        many=True,
        read_only=True,
    )

    class Meta:
        model = ProductVariantModel
        fields = (
            "id",
            "sku",
            "label",
            "price",
            "stock",
            "is_active",
            "attributes",
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
