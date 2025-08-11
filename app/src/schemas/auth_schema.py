from typing import Optional

from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchema(LoginSchema):
    first_name: Optional[str]
    last_name: Optional[str]


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenResponseSchema(BaseModel):
    access_token: str
