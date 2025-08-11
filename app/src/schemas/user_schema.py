from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        from_attributes = True


class UserRegisterResponse(BaseModel):
    # message: str
    user: UserResponse


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RegisterUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
