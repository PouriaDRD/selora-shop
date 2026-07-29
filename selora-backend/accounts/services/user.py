import logging

from django.db import IntegrityError
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError

from accounts.repositories import UserRepository

logger = logging.getLogger(__name__)

User = get_user_model()


class UserService:
    """
    Business logic for users.
    """

    @classmethod
    @transaction.atomic
    def create_user(
        cls,
        username: str,
        password: str,
        **extra_fields,
    ):
        """
        Create user.
        """

        username = username.strip().lower()

        if not username:
            raise ValidationError({"username": "Username is required."})

        try:
            user = UserRepository.create(
                username=username,
                password=password,
                **extra_fields,
            )

            logger.info(
                "User created successfully (%s)",
                user.username,
            )

            return user

        except IntegrityError:
            raise ValidationError(
                {"username": ("A user with this username already exists.")}
            )

        except Exception:
            logger.exception("Failed creating user.")
            raise

    @classmethod
    def update_last_login(
        cls,
        user,
    ):
        """
        Update last login timestamp.
        """

        user.last_login = timezone.now()

        UserRepository.update(
            user,
            update_fields=[
                "last_login",
            ],
        )
