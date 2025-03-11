from pydantic import ValidationError
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.exceptions.exception_heandlers import http_exception_handler, request_validation_exception_handler, validation_exception_handler, generic_exception_handler
from app.routers import transaction, user, login, wallet


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

# exceptions
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)

# routers
app.include_router(user.router)
app.include_router(login.router)
app.include_router(wallet.router)
app.include_router(transaction.router)


@app.get("/")
def read_root():
    return {"Hello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
