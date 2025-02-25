from pydantic import BaseModel, EmailStr, field_validator


class UserSchema(BaseModel):
    name: str
    nickname: str
    password: str
    email: EmailStr


    @field_validator("name", "nickname")
    def validate_name_and_nick(cls, value: str):
        if len(value.strip()) < 3:
            raise ValueError("name or nickname must have at least 3 characters")

        return value


class UserPublic(BaseModel):
    name: str
    nickname: str
    email: EmailStr
