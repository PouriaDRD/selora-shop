from rest_framework import serializers

from cart.models import CartModel

from .cart_item import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    total_price = serializers.SerializerMethodField()

    items_count = serializers.SerializerMethodField()

    class Meta:
        model = CartModel

        fields = [
            "id",
            "session_key",
            "items",
            "items_count",
            "total_price",
            "created_at",
            "updated_at",
        ]

    def get_items_count(self, obj):

        return obj.items.count()

    def get_total_price(self, obj):

        return sum(item.variant.price * item.quantity for item in obj.items.all())
