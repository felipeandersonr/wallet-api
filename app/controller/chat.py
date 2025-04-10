from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy import and_, exists, or_, select
from app.controller.base_controller import BaseController
from app.models.chat import Chat
from app.models.user import User
from app.utils.annotated import FilterPage


class ChatController(BaseController):
    def exists_chat(self, current_user_id: int, invited_user_id: int) -> bool:
        statement = select(exists().select_from(Chat)).where(
            or_(
                and_(
                    Chat.user_1_id == current_user_id,
                    Chat.user_2_id == invited_user_id
                ),
                
                and_(
                    Chat.user_1_id == invited_user_id,
                    Chat.user_2_id == current_user_id
                ), 

                Chat.is_active == True
            )
        )

        exists_chat = self.session.scalar(statement)

        return exists_chat
    
    
    def create_chat(self, current_user_id: int, invited_user_id: int) -> Chat:
        if current_user_id == invited_user_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="You cannot create a chat with yourself"
            )
        
        if self.exists_chat(current_user_id, invited_user_id):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Chat already exists"
            )
        
        new_chat = Chat(
            user_1_id=current_user_id,
            user_2_id=invited_user_id
        )

        self.session.add(new_chat)
        self.session.commit()

        return new_chat
        
    
    def delete_chat(self, chat_id: int, current_user_id: int):
        chat = self.get_chat(chat_id=chat_id, user_id=current_user_id)
        
        chat.deleted_by_user_1 = True if chat.user_1_id == current_user_id else chat.deleted_by_user_2 = True
    
        if chat.deleted_by_user_1 and chat.deleted_by_user_2:
            chat.is_active = False
        
        self.session.commit()

        return chat
    

    def get_chat(self, chat_id: int, user_id: int) -> Chat:
        statement = select(Chat).where(
            and_(
                Chat.id == chat_id, 

                or_(
                    and_(Chat.deleted_by_user_1 == False, Chat.user_1_id == user_id),
                    and_(Chat.deleted_by_user_2 == False, Chat.user_2_id == user_id),
                )
            )
        )
        
        chat = self.session.scalar(statement)

        if not chat:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Chat not found"
            )
        
        return chat
    

    def get_chats(self, is_active: bool = True, user_id: int = None, pagination: FilterPage = None, user_nickname: str = None) -> list[Chat]:
        statement = select(Chat)

        if user_id is not None:
            statement = statement.where(
                or_(
                    and_(Chat.deleted_by_user_1 == False, Chat.user_1_id == user_id),
                    and_(Chat.deleted_by_user_2 == False, Chat.user_2_id == user_id),
                )
            )

        if user_nickname is not None:
            statement = statement.join(User).where(User.nickname.ilike(f"%{user_nickname}%"))

            if not user_id:
                statement = statement.where(
                    or_(
                        and_(Chat.deleted_by_user_1 == False, Chat.user_1_id == user_id),
                        and_(Chat.deleted_by_user_2 == False, Chat.user_2_id == user_id),
                    )
                )

        if is_active:
            statement = statement.where(Chat.is_active == is_active)

        if pagination:
            statement = statement.offset(pagination.offset).limit(pagination.limit)

        chats = self.session.scalars(statement).all()

        return chats
