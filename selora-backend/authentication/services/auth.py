import logging
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

from .token import TokenService
from .login_history import LoginHistoryService


from cart.services import CartService
from accounts.services import UserService

logger = logging.getLogger("AuthService")


class AuthService:
    """
    Service layer for authentication business logic.
    Handles all business rules, validations, and orchestrates repository operations.
    """

    @classmethod
    def register(cls, username: str, password: str, request: Request, **extra_fields):
        """
        Register user with username and password.

        Args:
            username: The username to register.
            password: The password to register.
            request: The HTTP request object.

        Raises:
            ValidationError: If username is invalid, already exists, or other validation fails.

        Returns:
            Authentication response.
        """
        username = cls.normalize_username(username)
        session_key = extra_fields.get("session_key")
        extra_fields.pop("session_key")
        try:
            user = UserService.create_user(
                username=username, password=password, **extra_fields
            )

            LoginHistoryService.create_success(user, request)
            CartService.merge_guest_cart(user=user, session_key=session_key)

            return cls.auth_response(user)

        except ValidationError:
            raise

        except Exception as e:
            logger.exception(e)
            raise ValidationError("Failed to login user")

    @classmethod
    def login(cls, username: str, password: str, request: Request, **extra_fields):
        """
        Login user with username and password.

        Args:
            username: The username to login.
            password: The password to login.
            request: The HTTP request object.

        Returns:
            Authentication response.

        Raises:
            ValidationError: If username or password is invalid.
        """
        username = cls.normalize_username(username)
        session_key = extra_fields.get("session_key")
        extra_fields.pop("session_key")

        try:
            user = authenticate(
                request=request, username=username, password=password  # type: ignore
            )

            if not user:
                cls.handle_failed_login(
                    username=username,
                    request=request,
                    reason="نام کاربری یا رمز عبور اشتباه است.",
                )

                raise ValidationError("Invalid username or password.")

            LoginHistoryService.create_success(user, request)
            CartService.merge_guest_cart(user=user, session_key=session_key)

            return cls.auth_response(user)

        except ValidationError:
            raise

        except Exception as e:
            logger.exception(e)
            raise ValidationError("Failed to login user")

    @classmethod
    def handle_failed_login(cls, username: str, request: Request, reason: str):
        """
        Handle failed login.

        Args:
            username: The username that attempted to login.
            request: The HTTP request object.
            reason: Reason for login failure.

        """

        LoginHistoryService.create_failed(username, request, reason)

    @classmethod
    def normalize_username(cls, username: str):
        """
        Normalize the username by lowercasing the domain part of it.

        Args:
            username: The username to normalize.

        Returns:
            Normalized username.
        """
        return username.strip().lower()

    @classmethod
    def auth_response(cls, user):
        """
        Generate authentication response.

        Args:
            user: The authenticated user.

        Returns:
            Authentication response.
        """
        return {
            "user": str(user),
            **TokenService.generate(user),
        }
