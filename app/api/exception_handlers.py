from fastapi import Request
from fastapi.responses import JSONResponse

from app.shared.exceptions import AppError
from app.shared.schemas import ErrorResponse


async def app_error_handler(
    request: Request,
    exc: AppError,
) -> JSONResponse:
    response = ErrorResponse(
        error={
            "code": exc.code,
            "message": exc.message,
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
    )
