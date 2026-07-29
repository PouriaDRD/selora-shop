import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.throttling import ScopedRateThrottle

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from authentication.api.v1.serializers import RegisterSerializer
from config.swagger import (
    BAD_REQUEST_RESPONSE,
    THROTTLE_RESPONSE,
    SERVER_ERROR_RESPONSE,
)

logger = logging.getLogger("RegisterAPIView")


@extend_schema(
    tags=["Authentication"],
    summary="User Registration",
    description="""
Register a new user.

On successful registration, returns the newly created user. with access and refresh tokens.

Possible errors:
- Invalid credentials
- Validation errors
- Too many login attempts
""",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            description="Registered successfully.",
        ),
        400: BAD_REQUEST_RESPONSE,
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class RegisterAPIView(CreateAPIView):
    """
    Register a new user.
    """

    http_method_names = ["post"]

    serializer_class = RegisterSerializer

    permission_classes = [AllowAny]

    throttle_scope = "register"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        result = serializer.save()

        logger.info(f"User Registered successfully: {result['user']}")

        return Response(
            data=result,
            status=status.HTTP_201_CREATED,
        )
