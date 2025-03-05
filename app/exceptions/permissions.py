from http import HTTPStatus
from fastapi import HTTPException


class PermissionExceptions:
    def not_enought_permission(self):
        exception = HTTPException(
            detail="Not enough permissions",
            status_code=HTTPStatus.FORBIDDEN 
        )

        raise exception
    

permission_exceptions = PermissionExceptions()
