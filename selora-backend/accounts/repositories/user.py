from typing import Optional, List, Dict, Any
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from accounts.enums import UserRole, UserStatus

User = get_user_model()


class UserRepository:
    """
    Repository for User database operations.
    Handles all CRUD operations and queries for User model.
    """

    @staticmethod
    @transaction.atomic
    def create(**kwargs: Any):
        """
        Create a new user with atomic transaction.

        Args:
            **kwargs: User fields including username, password, email, etc.

        Returns:
            User: The created user instance.

        Raises:
            ValidationError: If the data is invalid.
        """
        try:
            return User.objects.create_user(**kwargs)
        except ValidationError as e:
            raise ValidationError(f"Failed to create user: {e}")

    @staticmethod
    def get_by_username(username: str):
        """
        Get a user by username.

        Args:
            username: The username to search for.

        Returns:
            Optional[User]: User instance or None if not found.
        """
        if not username:
            return None
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_id(id: str):
        """
        Get a user by ID.

        Args:
            user_id: The user ID (UUID or integer).

        Returns:
            Optional[User]: User instance or None if not found.
        """
        if not id:
            return None
        try:
            return User.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def update(user, update_fields: Optional[List[str]] = None):
        """
        Update user fields with atomic transaction.

        Args:
            user: The user instance to update.
            update_fields: List of field names to update. If None, all fields are saved.

        Returns:
            User: The updated user instance.

        Raises:
            ValidationError: If the data is invalid.
        """
        try:
            user.save(update_fields=update_fields)
            return user
        except ValidationError as e:
            raise ValidationError(f"Failed to update user: {e}")

    @staticmethod
    def get_all():
        """
        Get all users.

        Returns:
            QuerySet[User]: All user instances.
        """
        return User.objects.all()

    @staticmethod
    def get_by_role(role: UserRole):
        """
        Get all users with a specific role.

        Args:
            role: The user role to filter by.

        Returns:
            QuerySet[User]: Users with the specified role.
        """
        return User.objects.filter(role=role)

    @staticmethod
    def get_active_users():
        """
        Get all active users.

        Returns:
            QuerySet[User]: Active user instances.
        """
        return User.objects.filter(status=UserStatus.ACTIVE)

    @staticmethod
    def exists(username: Optional[str] = None) -> bool:
        """
        Check if a user exists with given username or email.

        Args:
            username: Optional username to check.

        Returns:
            bool: True if user exists, False otherwise.
        """
        query = {}
        if username:
            query["username"] = username

        if not query:
            return False

        return User.objects.filter(**query).exists()

    @staticmethod
    @transaction.atomic
    def delete(user) -> None:
        """
        Delete a user with atomic transaction.

        Args:
            user: The user instance to delete.
        """
        user.delete()

    @staticmethod
    @transaction.atomic
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
