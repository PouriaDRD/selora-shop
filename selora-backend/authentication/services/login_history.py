import logging
from user_agents import parse
from django.db import transaction
from rest_framework.request import Request

from accounts.repositories import UserRepository
from authentication.repositories import LoginHistoryRepository

logger = logging.getLogger("LoginHistoryService")


class LoginHistoryService:
    """
    Service for managing login history records.
    Handles creation of login attempts (successful and failed) with device information.
    """

    @staticmethod
    @transaction.atomic
    def create_success(user, request: Request):
        """
        Create a successful login history record.

        Args:
            user: The authenticated user.
            request: The HTTP request object.

        Returns:
            Created login history record.

        Raises:
            ValueError: If user or request is invalid.
        """
        if not user:
            logger.warning("Attempted to create success login without user")
            raise ValueError("User is required for successful login history")

        if not request:
            logger.warning("Attempted to create success login without request")
            raise ValueError("Request is required for login history")

        try:
            login_info = LoginHistoryService.get_login_info(request)

            login_record = LoginHistoryRepository.create(
                user=user,
                ip_address=login_info["ip_address"],
                user_agent=login_info["user_agent"],
                device=login_info["device"],
                browser=login_info["browser"],
                operating_system=login_info["os"],
                is_successful=True,
            )

            logger.info(
                f"Successful login recorded for user: {user.username} "
                f"from IP: {login_record.ip_address}"
            )

        except Exception as e:
            logger.error(
                f"Failed to create successful login history for user {user.username}: {str(e)}",
                exc_info=True,
            )
            raise e

    @staticmethod
    @transaction.atomic
    def create_failed(username: str, request: Request, reason: str):
        """
        Create a failed login attempt history record.

        Args:
            username: The username that attempted to login.
            request: The HTTP request object.
            reason: Reason for login failure.

        Returns:
            Created login history record or None.
        """

        if not username or not username.strip():
            logger.warning("Attempted to create failed login without username")
            return None

        if not request:
            logger.warning("Attempted to create failed login without request")
            return None

        try:
            user = UserRepository.get_by_username(username)
            if not user:
                return

            login_info = LoginHistoryService.get_login_info(request)

            login_record = LoginHistoryRepository.create(
                user=user,
                ip_address=login_info["ip_address"],
                user_agent=login_info["user_agent"],
                device=login_info["device"],
                browser=login_info["browser"],
                operating_system=login_info["os"],
                is_successful=False,
                failure_reason=reason,
            )
            logger.info(
                f"Failed login recorded for user: {username} "
                f"from IP: {login_record.ip_address} - Reason: {reason}"
            )

            return login_record

        except Exception as e:
            logger.error(
                f"Failed to create failed login history for user {username}: {str(e)}",
                exc_info=True,
            )
            raise e

    @staticmethod
    def get_login_info(request: Request):
        user_agent_string = request.META.get("HTTP_USER_AGENT", "")
        ua = parse(user_agent_string)

        os = ua.os.family

        browser = f"{ua.browser.family} {ua.browser.version_string}"
        device = "Mobile" if ua.is_mobile else "PC" if ua.is_pc else "Tablet"

        ip_address = LoginHistoryService.get_client_ip(request)

        return {
            "browser": browser,
            "device": device,
            "ip_address": ip_address,
            "user_agent": ua,
            "os": os,
        }

    @staticmethod
    def get_client_ip(request: Request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
