from http import HTTPStatus
from fastapi import APIRouter, Body

from app.controller.chat import ChatController
from app.shcemas.chat import ChatPublic, GetChatsFiltersModel
from app.utils.annotated import CurrentUser, GetSession


router = APIRouter(prefix="/chat", tags=["chats"])


@router.post("/create/{invited_user_id}", status_code=HTTPStatus.CREATED, response_model=ChatPublic)
def create_chat(user: CurrentUser, session: GetSession, invited_user_id: int):
    new_chat = ChatController(session=session).create_chat(
        current_user_id=user.id,
        invited_user_id=invited_user_id
    )

    return new_chat


@router.delete("/{chat_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_chat(chat_id: int, user: CurrentUser, session: GetSession):
    chat = ChatController(session=session).delete_chat(
        chat_id=chat_id,
        current_user_id=user.id
    )

    return chat


@router.post("/", status_code=HTTPStatus.OK, response_model=ChatPublic)
def get_chats(user: CurrentUser, session: GetSession, filters: GetChatsFiltersModel = Body(None)):
    chats = ChatController(session=session).get_chats(
        user_id=user.id,
        pagination=filters.pagination,
        user_nickname=filters.user_nickname
    )

    return chats


@router.get("/{chat_id}", status_code=HTTPStatus.OK, response_model=ChatPublic)
def get_chat(chat_id: int, user: CurrentUser, session: GetSession):
    chat = ChatController(session=session).get_chat(
        chat_id=chat_id,
        user_id=user.id
    )

    return chat
