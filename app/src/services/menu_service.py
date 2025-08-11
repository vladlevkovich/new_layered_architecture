from typing import List

from app.src.repository.menu_repository import MenuRepository
from app.src.schemas.menu_schema import MenuResponse


class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    async def menu(self) -> List[MenuResponse]:
        menu_items = await self.menu_repository.get_menu()
        return [
            MenuResponse(
                id=item.id,
                name=item.name,
                description=item.description,
                photo=item.photo,
                is_available=item.is_available,
            )
            for item in menu_items
        ]
