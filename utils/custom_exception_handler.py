from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler to return API responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "code": response.status_code,
            "message": response.data,  # Use the original response data which is already a dict
        }
        return response

    # If response is None, it means the exception was not handled by the default exception handler
    # In that case, we create our own response
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return Response(
        {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": str(exc)},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
