from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for UserModel.
    """

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "status",
            "last_login",
            "created_at",
        )

        read_only_fields = [
            "__all__",
        ]
