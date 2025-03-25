from http import HTTPStatus
from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.controller.chat import ChatController
from app.shcemas.chat import ChatPublic
from app.utils.annotated import CurrentUser, FilterPage, GetSession


router = APIRouter(prefix="/chat", tags=["chats"])


class CreateChatFiltersModel(BaseModel):
    invited_user_id: int


@router.post("/create", status_code=HTTPStatus.CREATED, response_model=ChatPublic)
def create_chat(user: CurrentUser, session: GetSession, filters: CreateChatFiltersModel = Body(...)):
    new_chat = ChatController(session=session).create_chat(
        current_user_id=user.id,
        invited_user_id=filters.invited_user_id
    )

    return new_chat


@router.delete("/{chat_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_chat(chat_id: int, user: CurrentUser, session: GetSession):
    chat = ChatController(session=session).delete_chat(
        chat_id=chat_id,
        current_user_id=user.id
    )

    return chat


class GetChatsFiltersModel(BaseModel):
    pagination: FilterPage
    user_nickname: str | None = None


@router.get("/", status_code=HTTPStatus.OK, response_model=ChatPublic)
def get_chats(user: CurrentUser, session: GetSession, filters: GetChatsFiltersModel = Body(None)):
    chats = ChatController(session=session).get_chats(
        user_id=user.id,
        pagination=filters.pagination
    )

    return chats
