from abc import ABC, abstractmethod
from typing import Optional

from app.src.core import auth
from app.src.models.user_models import User
from app.src.repository.user_repository import UserRepository
from app.src.schemas.auth_schema import LoginSchema, RegisterSchema
from app.src.schemas.user_schema import UserLoginResponse, UserOut
from app.src.utils.exceptions import InvalidCredentialsError, UserAlreadyExistsError


class BaseUserService(ABC):
    @abstractmethod
    async def register_user(self, user_data: RegisterSchema) -> User:
        """Register new user"""
        pass

    @abstractmethod
    async def login_user(self, login_data: LoginSchema) -> UserLoginResponse:
        """Login user"""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass


class UserService(BaseUserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: RegisterSchema) -> User:
        """Register new user"""
        # Check if user already exists
        existing_user = await self.user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsError("User with this email already exists")

        # Create new user
        user = User(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )

        return await self.user_repository.create(user)

    async def login_user(self, login_data: LoginSchema) -> UserLoginResponse:
        """Login user"""
        user = await self.user_repository.get_user_by_email(login_data.email)
        if not user:
            raise InvalidCredentialsError("Invalid email or password")

        # Create temporary user object for password verification
        temp_user = User(email=login_data.email, password=login_data.password)
        result = await self.user_repository.login(temp_user)

        if not result:
            raise InvalidCredentialsError("Invalid email or password")

        access_token = auth.create_access_token(
            UserOut.model_validate(result).model_dump()
        )
        refresh_token = auth.create_refresh_token(
            UserOut.model_validate(result).model_dump()
        )
        return UserLoginResponse(
            access_token=access_token, refresh_token=refresh_token
        )  # помилка BaseModel.__init__() takes 1 positional argument but 3 were given"

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return await self.user_repository.get_user_by_email(email)
