from abc import ABC, abstractmethod

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.models.user_models import User


class BaseUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """User create"""
        pass

    @abstractmethod
    async def login(self, user: User) -> User | None:
        """User login"""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        pass


class UserRepository(BaseUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __verify_password(self, password: str, hash_password: str) -> bool:
        return self.pwd_context.verify(password, hash_password)  # type: ignore

    def __get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)  # type: ignore

    async def create(self, user: User) -> User:
        user.password = self.__get_password_hash(user.password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def login(self, user: User) -> User | None:
        db_user = await self.get_user_by_email(user.email)
        if not db_user:
            return None

        if not self.__verify_password(user.password, db_user.password):
            return None

        return db_user

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.session.execute(select(User).where(User.email == email))
        return user.scalar_one_or_none()
