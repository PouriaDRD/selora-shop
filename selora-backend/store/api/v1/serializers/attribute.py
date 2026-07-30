from rest_framework import serializers

from store.models import AttributeModel, AttributeValueModel


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValueModel

        fields = [
            "id",
            "value",
        ]

        read_only_fields = ["__all__"]


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = AttributeModel

        fields = [
            "id",
            "name",
            "values",
        ]

        read_only_fields = ["__all__"]
