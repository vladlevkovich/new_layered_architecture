from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.models import Dish


class BaseMenuRepository(ABC):
    @abstractmethod
    async def get_menu(self) -> Sequence[Dish]:
        pass


class MenuRepository(BaseMenuRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_menu(self) -> Sequence[Dish]:
        smtp = await self.session.execute(select(Dish))
        result = smtp.scalars().all()
        return result
