import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors.base import AppError

logger = logging.getLogger(__name__)


async def app_error_handler(
    request: Request,
    exc: AppError,
) -> JSONResponse:
    logger.warning(
        "Application error request_id=%s method=%s path=%s code=%s",
        getattr(request.state, "request_id", None),
        request.method,
        request.url.path,
        exc.code,
    )

    error = {
        "code": exc.code,
        "message": exc.message,
    }

    if exc.details is not None:
        error["details"] = exc.details

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": error},
    )


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.info(
        "Request validation failed request_id=%s method=%s path=%s",
        getattr(request.state, "request_id", None),
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    if exc.status_code == 400:
        code = "BAD_REQUEST"
    elif exc.status_code == 401:
        code = "UNAUTHORIZED"
    elif exc.status_code == 403:
        code = "FORBIDDEN"
    elif exc.status_code == 404:
        code = "NOT_FOUND"
    elif exc.status_code == 405:
        code = "METHOD_NOT_ALLOWED"
    elif exc.status_code == 409:
        code = "CONFLICT"
    else:
        code = "HTTP_ERROR"

    message = exc.detail if isinstance(exc.detail, str) else "Request failed"

    logger.log(
        logging.WARNING if exc.status_code in {401, 403} else logging.INFO,
        "HTTP exception request_id=%s method=%s path=%s status_code=%s",
        getattr(request.state, "request_id", None),
        request.method,
        request.url.path,
        exc.status_code,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": message,
            }
        },
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unhandled exception request_id=%s method=%s path=%s",
        getattr(request.state, "request_id", None),
        request.method,
        request.url.path,
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            }
        },
    )
