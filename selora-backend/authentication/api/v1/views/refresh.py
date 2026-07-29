import logging
from typing import cast
from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import ScopedRateThrottle

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from config.swagger import (
    BAD_REQUEST_RESPONSE,
    UNAUTHORIZED_RESPONSE,
    THROTTLE_RESPONSE,
    SERVER_ERROR_RESPONSE,
)

logger = logging.getLogger("TokenRefreshAPIView")


@extend_schema(
    tags=["Authentication"],
    summary="Refresh JWT tokens",
    description="""
Generate a new JWT access token using a valid refresh token.

If refresh token rotation is enabled, a new refresh token is also returned.
""",
    request=TokenRefreshSerializer,
    responses={
        200: OpenApiResponse(
            description="Token refreshed successfully.",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": True,
                        "message": "The operation was successful",
                        "data": {
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "access_expires_at": "2026-07-29T16:15:42.491832+03:30",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh_expires_at": "2026-08-05T15:15:42.491832+03:30",
                        },
                    },
                )
            ],
        ),
        400: BAD_REQUEST_RESPONSE,
        401: UNAUTHORIZED_RESPONSE,
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class TokenRefreshAPIView(GenericAPIView):
    """
    Refresh JWT access token.
    """

    http_method_names = ["post"]

    permission_classes = [AllowAny]

    serializer_class = TokenRefreshSerializer

    throttle_scope = "refresh-token"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_lifetime = cast(
            timedelta,
            api_settings.ACCESS_TOKEN_LIFETIME,
        )
        access_expires_at = timezone.now() + access_lifetime

        refresh_lifetime = cast(
            timedelta,
            api_settings.REFRESH_TOKEN_LIFETIME,
        )
        refresh_expires_at = timezone.now() + refresh_lifetime

        logger.info("Token refreshed successfully.")

        return Response(
            data={
                "access": serializer.validated_data["access"],
                "access_expires_at": access_expires_at.isoformat(),
                "refresh": serializer.validated_data["refresh"],
                "refresh_expires_at": refresh_expires_at.isoformat(),
            },
            status=status.HTTP_200_OK,
        )
