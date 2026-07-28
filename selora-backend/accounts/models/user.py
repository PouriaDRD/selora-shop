import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.validators import user
from accounts.managers import UserManager
from accounts.enums import UserRole, UserStatus


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that replaces Django's default user model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Username is used for authentication
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and -/_ only.",
        validators=[user.username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    # user full name
    last_name = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)

    # Status for the user
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
        db_index=True,
    )

    # Role for the user
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
        db_index=True,
    )

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Custom manager
    objects = UserManager()

    # Use username for authentication
    USERNAME_FIELD = "username"
    # No REQUIRED_FIELDS needed since username is the only required field

    @property
    def is_staff(self) -> bool:
        """Check if the user has staff privileges."""
        return self.is_superuser or self.role in [
            UserRole.ADMIN,
        ]

    @property
    def is_active(self) -> bool:  # type: ignore
        """Override to check status instead of the default boolean field."""
        return self.status == UserStatus.ACTIVE

    @property
    def full_name(self) -> str:
        """Return the full name of the user."""
        name = f"{self.first_name} {self.last_name}".strip()
        if not name:
            return self.username
        return name

    def __str__(self) -> str:
        """String representation of the user."""
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status", "role"]),
            models.Index(fields=["created_at"]),
        ]
