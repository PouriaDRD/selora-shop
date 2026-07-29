from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from authentication.services import AuthService


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for registering a user.
    """

    username = serializers.CharField(
        required=True,
        write_only=True,
        min_length=3,
        max_length=150,
        error_messages={
            "required": "username is required",
            "blank": "username can not be blank",
        },
    )

    first_name = serializers.CharField(
        required=False,
        min_length=2,
        max_length=150,
        error_messages={
            "min_length": "first_name must be at least 2 characters long",
            "max_length": "first_name must be at most 150 characters long",
        },
    )

    last_name = serializers.CharField(
        required=False,
        min_length=2,
        max_length=150,
        error_messages={
            "min_length": "last_name must be at least 2 characters long",
            "max_length": "last_name must be at most 150 characters long",
        },
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        error_messages={
            "required": "password is required",
            "blank": "password can not be blank",
        },
    )

    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        error_messages={
            "required": "confirm_password is required",
            "blank": "confirm_password can not be blank",
        },
    )

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]

        if password != confirm_password:
            raise ValidationError({"confirm_password": "Passwords do not match."})

        try:
            validate_password(password)
        except Exception as e:
            raise ValidationError({"password": "Password is invalid."})

        attrs.pop("confirm_password")

        return attrs

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        request = self.context.get("request")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")

        result = AuthService.register(
            username=username,
            password=password,
            request=request,  # type: ignore
            first_name=first_name,
            last_name=last_name,
        )

        return result
