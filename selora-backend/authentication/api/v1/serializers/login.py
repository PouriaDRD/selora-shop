from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.services import AuthService


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    username = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            "required": "username is required",
            "blank": "username can not be blank",
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

    def validate(self, attrs):
        """
        Validate credentials via AuthService.
        """
        try:
            result = AuthService.login(
                username=attrs["username"],
                password=attrs["password"],
                request=self.context.get("request"),  # type: ignore
            )
        except:
            raise ValidationError(
                detail={"username": "Invalid username or password."},
                code="invalid_credentials",
            )

        attrs["auth_result"] = result
        return attrs
