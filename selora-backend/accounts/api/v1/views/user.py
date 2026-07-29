from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import OpenApiResponse, extend_schema

from ..serializers import UserSerializer

User = get_user_model()


@extend_schema(
    tags=["Accounts"],
    summary="Get current user profile",
    description="Returns the authenticated user's profile.",
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description="User profile retrieved successfully.",
        ),
    },
)
class UserProfileView(generics.RetrieveAPIView):
    """
    Retrieve authenticated user.
    """

    http_method_names = ["get"]

    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_object(self):  # type: ignore
        return self.request.user
