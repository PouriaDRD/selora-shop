from typing import Optional
from django.db import transaction
from django.db.models import QuerySet

from authentication.models import LoginHistoryModel


class LoginHistoryRepository:
    """
    Repository for LoginHistory database operations.
    Handles all CRUD operations and queries for LoginHistory model.
    """

    @staticmethod
    @transaction.atomic
    def create(**data) -> LoginHistoryModel:

        return LoginHistoryModel.objects.create(**data)

    @staticmethod
    def get_user_history(user_id) -> QuerySet[LoginHistoryModel]:

        return LoginHistoryModel.objects.filter(user_id=user_id).order_by("-created_at")

    @staticmethod
    def get_last_login(user) -> Optional[LoginHistoryModel]:
        """Get the most recent login for a user."""
        return (
            LoginHistoryModel.objects.filter(user=user).order_by("-created_at").first()
        )

    @staticmethod
    def get_user_history_count(
        user_id,
    ) -> int:

        return LoginHistoryModel.objects.filter(user_id=user_id).count()
