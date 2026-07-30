from rest_framework import serializers

from cart.models import CartItemModel


class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="variant.product.name",
        read_only=True,
    )

    variant_label = serializers.CharField(
        source="variant.label",
        read_only=True,
    )

    variant_id = serializers.UUIDField(
        source="variant.id",
        read_only=True,
    )

    price = serializers.IntegerField(
        source="variant.price",
        read_only=True,
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItemModel

        fields = [
            "id",
            "product_name",
            "variant_label",
            "variant_id",
            "price",
            "quantity",
            "subtotal",
        ]

    def get_subtotal(self, obj):

        return obj.variant.price * obj.quantity


class CartAddItemSerializer(serializers.Serializer):
    cart_session_key = serializers.CharField(max_length=64)

    variant_id = serializers.UUIDField()

    quantity = serializers.IntegerField(
        min_value=1,
        default=1,
    )


class CartUpdateItemSerializer(serializers.Serializer):

    quantity = serializers.IntegerField(
        min_value=1,
    )
