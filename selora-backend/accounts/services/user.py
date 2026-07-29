import logging
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


from accounts.repositories import UserRepository

logger = logging.getLogger("UserService")
User = get_user_model()


class UserService:
    """
    Service layer for User business logic.
    Handles all business rules, validations, and orchestrates repository operations.
    """

    @classmethod
    @transaction.atomic
    def create_user(cls, username: str, password: str, **extra_fields):
        """
        Create a new user with validation and business rules.

        Args:
            username: Unique username for the user.
            password: User's password (will be hashed).
            **extra_fields: Additional fields like first_name, last_name, role, etc.

        Returns:
            User: The newly created user instance.

        Raises:
            ValidationError: If username is invalid, already exists, or other validation fails.
        """
        # Validate and normalize username
        username = username.strip().lower()
        if not username or not username.strip():
            raise ValidationError({"username": "Username is required."})

        # Check for existing user
        if UserRepository.exists(username=username):
            raise ValidationError(
                {"username": "A user with this username already exists."}
            )

        try:
            # Create the user
            new_user = UserRepository.create(
                username=username, password=password, **extra_fields
            )

            logger.info(f"User created successfully: {username} (ID: {new_user.id})")  # type: ignore
            return new_user

        except Exception as e:
            logger.error(f"Failed to create user {username}: {str(e)}")
            raise ValidationError(f"Failed to create user: {str(e)}")

    @classmethod
    @transaction.atomic
    def update_last_login(cls, user) -> None:
        """
        Update the last login timestamp for a user.

        Args:
            user: The user instance to update.
        """
        if not user:
            raise ValidationError("User object is required.")

        try:
            user.last_login = timezone.now()
            UserRepository.update(user, update_fields=["last_login"])
            logger.debug(f"Updated last_login for user: {user.username}")
        except Exception as e:
            logger.error(f"Failed to update last_login for {user.username}: {str(e)}")
            raise ValidationError(f"Failed to update last login: {str(e)}")
