import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from authentication.repositories import LoginHistoryRepository
from authentication.api.v1.serializers import LoginHistorySerializer

logger = logging.getLogger("MyLoginHistoryAPIView")


class MyLoginHistoryAPIView(ListAPIView):
    """
    API endpoint for user login history.
    """

    http_method_names = ["get"]

    permission_classes = [IsAuthenticated]
    serializer_class = LoginHistorySerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore

        return LoginHistoryRepository.get_user_history(str(self.request.user.id))  # type: ignore
