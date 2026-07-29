import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_login_failed,
)
from django.dispatch import receiver

from authentication.services import LoginHistoryService

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def handle_successful_login(
    sender,
    request,
    user,
    **kwargs,
):
    """
    Triggered automatically after Django login succeeds.
    """

    try:
        LoginHistoryService.create_success(
            user=user,
            request=request,
        )

    except Exception:
        logger.exception(
            "Failed creating login history for user: %s",
            user.username,
        )


@receiver(user_login_failed)
def handle_failed_login(
    sender,
    credentials,
    request,
    **kwargs,
):
    """
    Triggered automatically when login fails.
    """

    username = credentials.get("username")

    try:
        LoginHistoryService.create_failed(
            username=username,
            request=request,
        )  # type: ignore

    except Exception:
        logger.exception("Failed saving failed login history")
