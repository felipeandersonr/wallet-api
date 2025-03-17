from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy import and_, exists, or_, select
from app.controller.base_controller import BaseController
from app.models.friendship import Friendship
from app.models.user import User
from app.utils.annotated import FilterPage


class FriendshipController(BaseController):
    def create_friendship_request(self, friend_id: int, current_user_id: int) -> Friendship:
        if friend_id == current_user_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="You cannot send a friendship request to yourself"
            )
    
        statement = select(exists().where(User.id == friend_id))
        exists_user = self.session.scalar(statement)

        if not exists_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not found"
            )
        
        exists_friendship_statement = select(exists().select_from(Friendship).where(
            or_(
                and_(Friendship.user_id == current_user_id, Friendship.friend_id == friend_id), 
                and_(Friendship.user_id == friend_id, Friendship.friend_id == current_user_id),
            ),

            or_(
                Friendship.status == "pending",
                Friendship.status == "accepted"
            ),
            
            Friendship.is_active == True
            )
        )

        exists_friendship = self.session.scalar(exists_friendship_statement)

        if exists_friendship:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Friendship request already exists"
            )
        
        new_friendship = Friendship(
            status="pending",
            friend_id=friend_id, 
            user_id=current_user_id
        )

        self.session.add(new_friendship)
        self.session.commit()   

        return new_friendship


    def accept_friendship_request(self, friendship_id: int) -> Friendship:
        friendship = self.session.scalar(
            select(Friendship).where(
                Friendship.id == friendship_id, 
                Friendship.status == "pending", 
                Friendship.is_active == True
            )
        )

        if not friendship:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Friendship request not found"
            )
        
        friendship.status = "accepted"
        self.session.commit()

        return friendship
        

    def reject_friendship_request(self, friendship_id: int) -> Friendship:
        friendship = self.session.scalar(
            select(Friendship).where(
                Friendship.id == friendship_id, 
                Friendship.status == "pending", 
                Friendship.is_active == True
            )
        )   

        if not friendship:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Friendship request not found"
            )   
        
        friendship.status = "rejected"
        self.session.commit()

        return friendship
    

    def get_friendships(self, 
                        user_id: int, 
                        accepted_status: bool = True, 
                        rejected_status: bool = True, 
                        pedding_status: bool = True, 
                        is_active: bool = True, 
                        pagination: FilterPage | None = None) -> list[Friendship]:
        
        statement = select(Friendship)

        if pedding_status:
            statement = statement.where(Friendship.status == "pending")

        if accepted_status:
            statement = statement.where(Friendship.status == "accepted")

        if rejected_status:
            statement = statement.where(Friendship.status == "rejected")

        if is_active:
            statement = statement.where(Friendship.is_active == is_active)

        if user_id: 
            statement = statement.where(or_(Friendship.user_id == user_id, Friendship.friend_id == user_id))

        if pagination:
            statement = statement.offset(pagination.offset).limit(pagination.limit)

        statement = statement.distinct()

        friendships = self.session.scalars(statement).all()

        return friendships
