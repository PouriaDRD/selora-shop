# config/swagger.py

from drf_spectacular.utils import OpenApiExample, OpenApiResponse

# ------------------------------------------------------------------
# 400 Bad Request
# ------------------------------------------------------------------

BAD_REQUEST_RESPONSE = OpenApiResponse(
    description="Validation failed.",
    examples=[
        OpenApiExample(
            "Validation Error",
            value={
                "status": False,
                "message": "Field phone_number: This field is required.",
                "data": [],
                "errors": {"phone_number": ["This field is required."]},
            },
        )
    ],
)

# ------------------------------------------------------------------
# 401 Unauthorized
# ------------------------------------------------------------------

UNAUTHORIZED_RESPONSE = OpenApiResponse(
    description="Authentication failed.",
    examples=[
        OpenApiExample(
            "Unauthorized",
            value={
                "status": False,
                "message": "Authentication credentials were not provided.",
                "data": [],
                "errors": {"detail": "Authentication credentials were not provided."},
            },
        ),
        OpenApiExample(
            "Invalid Token",
            value={
                "status": False,
                "message": "Given token not valid for any token type.",
                "data": [],
                "errors": {"detail": "Given token not valid for any token type."},
            },
        ),
    ],
)

# ------------------------------------------------------------------
# 403 Forbidden
# ------------------------------------------------------------------

FORBIDDEN_RESPONSE = OpenApiResponse(
    description="Permission denied.",
    examples=[
        OpenApiExample(
            "Forbidden",
            value={
                "status": False,
                "message": "You do not have permission to perform this action.",
                "data": [],
                "errors": {
                    "detail": "You do not have permission to perform this action."
                },
            },
        )
    ],
)

# ------------------------------------------------------------------
# 404 Not Found
# ------------------------------------------------------------------

NOT_FOUND_RESPONSE = OpenApiResponse(
    description="Resource not found.",
    examples=[
        OpenApiExample(
            "Not Found",
            value={
                "status": False,
                "message": "Not found.",
                "data": [],
                "errors": {"detail": "Not found."},
            },
        )
    ],
)

# ------------------------------------------------------------------
# 409 Conflict
# ------------------------------------------------------------------

CONFLICT_RESPONSE = OpenApiResponse(
    description="Database constraint violation or resource conflict.",
    examples=[
        OpenApiExample(
            "Conflict",
            value={
                "status": False,
                "message": "Database constraint violation or conflict.",
                "data": [],
                "errors": {"detail": "Database constraint violation or conflict."},
            },
        )
    ],
)

# ------------------------------------------------------------------
# 429 Too Many Requests
# ------------------------------------------------------------------

THROTTLE_RESPONSE = OpenApiResponse(
    description="Request throttled.",
    examples=[
        OpenApiExample(
            "Too Many Requests",
            value={
                "status": False,
                "message": "Request was throttled.",
                "data": [],
                "errors": {
                    "detail": (
                        "Request was throttled. " "Expected available in 60 seconds."
                    )
                },
            },
        )
    ],
)

# ------------------------------------------------------------------
# 500 Internal Server Error
# ------------------------------------------------------------------

SERVER_ERROR_RESPONSE = OpenApiResponse(
    description="Unexpected server error.",
    examples=[
        OpenApiExample(
            "Internal Server Error",
            value={
                "status": False,
                "message": "A server error occurred. Please contact support.",
                "data": [],
                "errors": {
                    "detail": "A server error occurred. Please contact support."
                },
            },
        )
    ],
)
