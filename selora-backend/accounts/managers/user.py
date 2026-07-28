from typing import Optional
from django.contrib.auth.models import BaseUserManager
from accounts.enums import UserRole, UserStatus


class UserManager(BaseUserManager):
    """Custom manager for the UserModel, handling user and superuser creation."""

    def create_user(
        self, username: str, password: Optional[str] = None, **extra_fields
    ):
        """
        Create a new user with the given username and password.

        Args:
            username: The username for the new user (required)
            password: Optional password (if not provided, sets unusable password for OAuth)
            **extra_fields: Additional fields for the user model

        Returns:
            UserModel: The created user instance
        """
        if not username:
            raise ValueError("The username field must be set.")

        # Clean and normalize username
        username = self.model.normalize_username(username)

        # Create user instance
        user = self.model(
            username=username,
            is_superuser=False,
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
            **extra_fields
        )

        # Set password or mark as unusable for OAuth
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(
        self, username: str, password: Optional[str] = None, **extra_fields
    ):
        """
        Create a new superuser with the given username and password.

        Args:
            username: The username for the superuser (required)
            password: Password for the superuser (required)
            **extra_fields: Additional fields for the user model

        Returns:
            UserModel: The created superuser instance
        """
        # Ensure superuser has a password
        if not password:
            raise ValueError("Superusers must have a password.")

        # Create a normal user
        user = self.create_user(username=username, password=password, **extra_fields)

        # Grant superuser permissions
        user.is_superuser = True
        user.role = UserRole.SUPERUSER
        user.status = UserStatus.ACTIVE

        user.save(using=self._db)

        return user

    def get_by_natural_key(self, username):
        """Required for Django's authentication backend."""
        return self.get(username=username)
