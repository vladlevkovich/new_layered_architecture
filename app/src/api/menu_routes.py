from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.src.containers.container import Container
from app.src.schemas.menu_schema import MenuResponse
from app.src.services import MenuService

router = APIRouter(prefix="/menu")


@router.get("", response_model=List[MenuResponse])
@inject
async def get_menu(
    request: Request,
    menu_service: MenuService = Depends(Provide[Container.menu_service]),
) -> List[MenuResponse]:
    # print(user)
    print(list(request))
    print(request.state)
    print(request.state.user)
    return await menu_service.menu()
