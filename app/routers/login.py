from fastapi import APIRouter

from app.utils.annotated import CurrentUser, GetSession, OAuth2Form
from app.controller.login import LoginController
from app.shcemas.login import TokenPublic
from app.shcemas.generic import Message
from app.exceptions.permissions import permission_exceptions


router = APIRouter(prefix="/auth", tags=["token"])


@router.post("/login", response_model=TokenPublic)
def login(session: GetSession, form_data: OAuth2Form) -> TokenPublic:
    token = LoginController(session).login(form_data)

    return token


@router.delete("/logout/{user_id}", response_model=Message)
def logout(user_id: int, session: GetSession, user: CurrentUser):
    if user.id != user_id:
        permission_exceptions.not_enought_permission()
    
    LoginController(session).logout(user_id)

    message = {"message": "Authorization token deleted"}

    return message
