import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.exceptions import http_exception_handler, validation_exception_handler, generic_exception_handler
from app.routers import user


app = FastAPI()

# exceptions
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# routers
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"Hello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
