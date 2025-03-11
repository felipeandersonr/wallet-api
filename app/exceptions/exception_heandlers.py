from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    exception = JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status": "Failed"
        }
    )

    return exception


async def validation_exception_handler(request: Request, exc: ValidationError):
    detail_str = exc.errors()[0]["msg"]

    exception = JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": detail_str
        }
    )

    return exception


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    detail_str = str(exc.errors()[0]["msg"]) if exc.errors() else "Invalid input"
    
    exception = JSONResponse(
        status_code=422,
        content={
            "details": detail_str,
            "error": "Validation Error",
        }
    )
    
    return exception


async def generic_exception_handler(request: Request, exc: Exception):
    exception = JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error"}
    )

    return exception
