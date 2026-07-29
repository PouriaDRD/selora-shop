from typing import Any, List, Dict
from django.contrib.auth import get_user_model

from accounts.enums import UserRole, UserStatus

User = get_user_model()


class UserRepository:
    """
    Repository responsible only for database operations on UserModel.
    No business logic or transaction management should exist here.
    """

    @staticmethod
    def create(**kwargs: Any):
        """
        Create a new user.

        Raises:
            IntegrityError
            ValidationError
        """
        return User.objects.create_user(**kwargs)

    @staticmethod
    def update(user, update_fields=None):
        """
        Persist changes for a user.
        """
        user.save(update_fields=update_fields)
        return user

    @staticmethod
    def delete(user) -> None:
        """
        Delete a user.
        """
        user.delete()

    @staticmethod
    def get_by_id(user_id):
        """
        Retrieve user by id.
        """
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def get_by_username(username: str):
        """
        Retrieve user by username.
        """
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_all():
        """
        Return all users.
        """
        return User.objects.all()

    @staticmethod
    def get_active():
        """
        Return active users.
        """
        return User.objects.filter(status=UserStatus.ACTIVE)

    @staticmethod
    def get_by_role(role: UserRole):
        """
        Return users by role.
        """
        return User.objects.filter(role=role)

    @staticmethod
    def exists(username: str) -> bool:
        """
        Check if username already exists.
        """
        return User.objects.filter(username=username).exists()

    @staticmethod
    def bulk_create(users_data: List[Dict[str, Any]]):
        """
        Create multiple users in bulk.

        Args:
            users_data: List of user data dictionaries.

        Returns:
            List[User]: List of created user instances.
        """
        users = [User(**data) for data in users_data]
        return User.objects.bulk_create(users)
