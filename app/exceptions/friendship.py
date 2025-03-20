from http import HTTPStatus
from fastapi import HTTPException


class FriendshipException:
    def friendship_required(self):
        exception = HTTPException(
            detail="Friendship required",
            status_code=HTTPStatus.FORBIDDEN
        )

        raise exception


friendship_exceptions = FriendshipException()
