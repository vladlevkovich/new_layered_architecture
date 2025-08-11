from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.src.containers.container import Container
from app.src.schemas.order_shema import OrderCreateResponse, OrderSchema
from app.src.services import OrderService

router = APIRouter(prefix="/order")


@router.post("", response_model=OrderCreateResponse)
@inject
async def create_order(
    request: Request,
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> OrderCreateResponse:  # -> Order
    return await order_service.create_order(
        request.state.user["id"], request.state.user["email"]
    )


@router.get("/order-detail", response_model=OrderSchema)
@inject
async def get_order_detail(
    request: Request,
    order_service: OrderService = Depends(Provide[Container.order_service]),
) -> OrderSchema:
    return await order_service.get_order_detail(request.state.user["id"])
