import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import ScopedRateThrottle

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from authentication.api.v1.serializers import LoginSerializer

from config.swagger import (
    BAD_REQUEST_RESPONSE,
    THROTTLE_RESPONSE,
    SERVER_ERROR_RESPONSE,
)

logger = logging.getLogger("LoginAPIView")


@extend_schema(
    tags=["Authentication"],
    summary="User login",
    description="""
Authenticate user with username and password.

On successful authentication, returns access and refresh tokens.

Possible errors:
- Invalid credentials
- Validation errors
- Too many login attempts
""",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Login successful.",
        ),
        400: BAD_REQUEST_RESPONSE,
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class LoginAPIView(GenericAPIView):
    """
    User login endpoint.
    """

    serializer_class = LoginSerializer

    permission_classes = [AllowAny]

    throttle_scope = "login"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    http_method_names = [
        "post",
    ]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        auth_result = serializer.validated_data["auth_result"]

        return Response(
            data={
                "user": auth_result["user"],
                "access": auth_result["access"],
                "refresh": auth_result["refresh"],
                "access_expires_at": auth_result["access_expires_at"],
                "refresh_expires_at": auth_result["refresh_expires_at"],
            },
            status=status.HTTP_200_OK,
        )
