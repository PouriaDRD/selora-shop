import re
from django.core.exceptions import ValidationError


def username_validator(value):
    """Validate username contains only allowed characters."""
    if not re.match(r"^[a-zA-Z0-9_-]+$", value):
        raise ValidationError(
            "Invalid character in the username. Only English letters, numbers, hyphens, and underscores are allowed.",
            code="invalid_username",
        )
