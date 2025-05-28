from fastapi import Request, status
from fastapi.responses import JSONResponse

from delivery_service.application.exceptions import (
    ApplicationError, BoxNotFoundError, CacheError,
    ExchangeRateNotAvailableError, MessageQueueError)


async def app_error_handler(
    request: Request, exc: ApplicationError
) -> JSONResponse:
    """
    Maps application errors to HTTP status codes and response format.
    """
    if isinstance(exc, BoxNotFoundError):
        http_status = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, ExchangeRateNotAvailableError):
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    elif isinstance(exc, CacheError):
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    elif isinstance(exc, MessageQueueError):
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    elif isinstance(exc, ApplicationError):
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    return JSONResponse(
        status_code=http_status,
        content={
            "detail": [
                {
                    "msg": str(exc),
                    "type": exc.__class__.__name__,
                }
            ]
        },
    )
