from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from authentication.repositories import (
    LoginHistoryRepository,
)

from authentication.api.v1.serializers import (
    LoginHistorySerializer,
)

from config.swagger import (
    THROTTLE_RESPONSE,
    SERVER_ERROR_RESPONSE,
)


@extend_schema(
    tags=["Authentication"],
    summary="Get my login history",
    description="""
Retrieve the authenticated user's login history.

This endpoint provides information about previous login attempts,
including login timestamps, IP addresses, and device information.

Authentication:
- Requires a valid authenticated user.

Possible errors:
- Unauthorized access.
- Too many requests.
- Server errors.
""",
    responses={
        200: OpenApiResponse(
            response=LoginHistorySerializer(many=True),
            description="Login history retrieved successfully.",
        ),
        401: OpenApiResponse(
            description="Authentication credentials were not provided or invalid.",
        ),
        429: THROTTLE_RESPONSE,
        500: SERVER_ERROR_RESPONSE,
    },
)
class MyLoginHistoryAPIView(ListAPIView):
    """
    API endpoint for retrieving the authenticated user's login history.

    Returns:
        A list of previous login records belonging to the current user.

    Permissions:
        Requires authentication.

    Throttling:
        Uses user scoped rate limiting.

    Repository:
        LoginHistoryRepository.get_user_history()
    """

    http_method_names = [
        "get",
    ]

    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = LoginHistorySerializer

    throttle_scope = "user"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def get_queryset(self):  # type: ignore
        """
        Retrieve login history for the current authenticated user.

        Returns:
            QuerySet:
                Login history records for the current user.
        """

        return LoginHistoryRepository.get_user_history(
            str(self.request.user.id)  # type: ignore
        )
