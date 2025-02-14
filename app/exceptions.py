from fastapi import HTTPException, Request
from pydantic import ValidationError
from starlette.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    exception = JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status": "failed"
        }
    )

    return exception


async def validation_exception_handler(request: Request, exc: ValidationError):
    exception = JSONResponse(
        status_code=422,
        content={
            "error": "validation error",
            "details": exc.errors()
        }
    )

    return exception


async def generic_exception_handler(request: Request, exc: Exception):
    exception = JSONResponse(
        status_code=500,
        content={"error": "internal server error"}
    )

    return exception
