from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.src.containers.container import Container
from app.src.schemas.cart_schema import (
    CartItemCreate,
    CartItemOutResponseSchema,
    CartItemOutSchema,
    CartOut,
)
from app.src.services import CartService

router = APIRouter(prefix="/cart")


@router.get("", response_model=CartOut)
@inject
async def get_user_cart(
    request: Request,
    cart_service: CartService = Depends(Provide[Container.cart_service]),
) -> CartOut:
    cart = await cart_service.get_cart(request.state.user['"id'])
    return CartOut(
        id=cart.id, user_id=request.state.user['"id'], updated_at=cart.updated_at
    )


@router.post("/create", response_model=CartOut)
@inject
async def cart_create(
    request: Request,
    cart_service: CartService = Depends(Provide[Container.cart_service]),
) -> CartOut:
    return await cart_service.create_cart(request.state.user['"id'])


@router.post("/item", response_model=CartItemOutResponseSchema)
@inject
async def add_item_to_cart(
    item_data: CartItemCreate,
    request: Request,
    cart_service: CartService = Depends(Provide[Container.cart_service]),
) -> CartItemOutResponseSchema:
    cart = await cart_service.get_cart(request.state.user['"id'])
    return await cart_service.add_item_to_cart(cart, item_data)


@router.get("/items", response_model=CartItemOutSchema)
@inject
async def get_items(
    request: Request,
    cart_service: CartService = Depends(Provide[Container.cart_service]),
) -> CartItemOutSchema:
    cart = await cart_service.get_cart(request.state.user['"id'])
    return await cart_service.items(cart.id)
