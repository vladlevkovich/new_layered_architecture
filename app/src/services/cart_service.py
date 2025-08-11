from fastapi import HTTPException

from app.src.models import Cart
from app.src.repository import CartRepository
from app.src.schemas.cart_schema import (
    CartItemCreate,
    CartItemOutResponseSchema,
    CartItemOutSchema,
    CartOut,
)


class CartService:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    async def get_cart(self, user_id: int) -> Cart:
        cart = await self.cart_repository.get_user_cart(user_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart

    async def create_cart(self, user_id: int) -> CartOut:
        cart = await self.cart_repository.create_cart_for_user(user_id)
        return CartOut(id=cart.id, user_id=user_id, updated_at=cart.updated_at)

    async def add_item_to_cart(
        self, cart: Cart, item_data: CartItemCreate
    ) -> CartItemOutResponseSchema:
        item = await self.cart_repository.add_item(cart, item_data)
        return CartItemOutResponseSchema.model_validate(item)

    async def items(self, cart_id: int) -> CartItemOutSchema:
        items = await self.cart_repository.get_items(cart_id)
        total_sum = sum(item.dish.price * item.quantity for item in items)
        return CartItemOutSchema(dish=items, total_price=total_sum)
