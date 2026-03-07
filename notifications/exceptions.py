"""
Custom DRF Exception Handler
============================
Returns a consistent error shape for every API error response.

All errors look like this:
{
    "success": false,
    "error": {
        "code":    "VALIDATION_ERROR",       # machine-readable error type
        "message": "One or more fields...",  # human-readable summary
        "details": { ... }                   # field-level detail (optional)
    }
}

SETUP
-----
In settings.py add:

    REST_FRAMEWORK = {
        "EXCEPTION_HANDLER": "yourapp.exceptions.custom_exception_handler"
    }
"""

import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied as DRFPermissionDenied,
    Throttled,
    UnsupportedMediaType,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_default_handler

logger = logging.getLogger(__name__)


# ── Error code mapping ──────────────────────────────────────────────────────
# Maps DRF exception classes to a clean machine-readable code string.

EXCEPTION_CODE_MAP = {
    ValidationError:        "VALIDATION_ERROR",
    NotFound:               "NOT_FOUND",
    Http404:                "NOT_FOUND",
    AuthenticationFailed:   "AUTHENTICATION_FAILED",
    NotAuthenticated:       "NOT_AUTHENTICATED",
    DRFPermissionDenied:    "PERMISSION_DENIED",
    PermissionDenied:       "PERMISSION_DENIED",
    MethodNotAllowed:       "METHOD_NOT_ALLOWED",
    Throttled:              "THROTTLED",
    ParseError:             "PARSE_ERROR",
    UnsupportedMediaType:   "UNSUPPORTED_MEDIA_TYPE",
}

# ── Human-readable default messages ────────────────────────────────────────

DEFAULT_MESSAGES = {
    "VALIDATION_ERROR":      "One or more fields are invalid.",
    "NOT_FOUND":             "The requested resource was not found.",
    "AUTHENTICATION_FAILED": "Authentication credentials are invalid.",
    "NOT_AUTHENTICATED":     "Authentication credentials were not provided.",
    "PERMISSION_DENIED":     "You do not have permission to perform this action.",
    "METHOD_NOT_ALLOWED":    "This HTTP method is not allowed.",
    "THROTTLED":             "Too many requests. Please slow down.",
    "PARSE_ERROR":           "Malformed request body.",
    "UNSUPPORTED_MEDIA_TYPE":"Unsupported media type.",
    "SERVER_ERROR":          "An unexpected server error occurred.",
}


# ── Main handler ────────────────────────────────────────────────────────────

def custom_exception_handler(exc, context):
    """
    Replacement for DRF's default exception handler.

    Always returns:
        {
            "success": false,
            "error": {
                "code":    str,
                "message": str,
                "details": dict | list | None
            }
        }
    """

    # 1. Let DRF do its first-pass processing.
    #    This converts Django's Http404 / PermissionDenied into DRF responses
    #    and populates response.data with its default error dict.
    response = drf_default_handler(exc, context)

    # 2. If DRF returned None the exception is unhandled (e.g. a plain
    #    Python exception or a 500).  We still want to return a consistent
    #    shape rather than letting Django's HTML error page leak through.
    if response is None:
        logger.exception(
            "Unhandled exception in %s",
            context.get("view", "unknown view"),
            exc_info=exc,
        )
        return Response(
            _build_error_body("SERVER_ERROR", details=None),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # 3. Determine the error code for this exception type.
    code = _resolve_code(exc)

    # 4. Extract the human-readable summary and field-level details.
    message, details = _extract_message_and_details(exc, code, response.data)

    # 5. Replace response.data with the consistent envelope.
    response.data = _build_error_body(code, message, details)

    return response


# ── Helpers ─────────────────────────────────────────────────────────────────

def _build_error_body(code, message=None, details=None):
    """Return the standard error envelope dict."""
    return {
        "success": False,
        "error": {
            "code":    code,
            "message": message or DEFAULT_MESSAGES.get(code, "An error occurred."),
            "details": details,
        },
    }


def _resolve_code(exc):
    """
    Walk the EXCEPTION_CODE_MAP in MRO order so subclasses are matched
    before their parents.  Falls back to 'SERVER_ERROR'.
    """
    for exc_class, code in EXCEPTION_CODE_MAP.items():
        if isinstance(exc, exc_class):
            return code
    return "SERVER_ERROR"


def _extract_message_and_details(exc, code, data):
    """
    Return (message: str, details: dict | list | None).

    - For ValidationError the top-level 'detail' is used as the summary
      message and the field dict becomes 'details'.
    - For other errors 'detail' is the message and 'details' is None.
    """
    if code == "VALIDATION_ERROR":
        # data looks like:
        #   {"field": ["msg1"], "other": ["msg2"]}          ← field errors
        #   {"non_field_errors": ["msg"]}                   ← non-field errors
        #   ["msg"]                                         ← list-level errors

        if isinstance(data, dict):
            # Separate non_field_errors from field errors
            non_field = data.pop("non_field_errors", None)

            # non_field_errors → use as the top-level message
            if non_field:
                message = _coerce_to_str(non_field)
            else:
                message = DEFAULT_MESSAGES["VALIDATION_ERROR"]

            # Remaining keys are field-level errors
            details = _stringify_error_dict(data) if data else None
        elif isinstance(data, list):
            message = _coerce_to_str(data)
            details = None
        else:
            message = str(data)
            details = None

        return message, details

    if code == "THROTTLED":
        # DRF adds a 'wait' key with the number of seconds until retry
        wait = getattr(exc, "wait", None)
        message = DEFAULT_MESSAGES["THROTTLED"]
        details = {"retry_after_seconds": int(wait)} if wait else None
        return message, details

    # All other cases: 'detail' holds either a string or ErrorDetail
    detail = data.get("detail", "") if isinstance(data, dict) else str(data)
    return str(detail), None


def _stringify_error_dict(data):
    """
    Convert a dict of ErrorDetail lists into plain string lists so the
    response is JSON-serialisable without DRF-specific objects.
    """
    result = {}
    for field, errors in data.items():
        if isinstance(errors, list):
            result[field] = [str(e) for e in errors]
        elif isinstance(errors, dict):
            result[field] = _stringify_error_dict(errors)   # nested serializer
        else:
            result[field] = str(errors)
    return result


def _coerce_to_str(value):
    """Turn a list or ErrorDetail into a plain string."""
    if isinstance(value, list):
        return " ".join(str(v) for v in value)
    return str(value)
