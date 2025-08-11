from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.src.models.cart_models import Cart, CartItem
from app.src.schemas.cart_schema import CartItemCreate


class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_cart(self, user_id: int) -> Cart | None:
        result = await self.session.execute(select(Cart).where(Cart.user_id == user_id))
        return result.scalars().first()

    async def create_cart_for_user(self, user_id: int) -> Cart:
        cart = Cart(user_id=user_id)
        self.session.add(cart)
        await self.session.commit()
        return cart

    async def add_item(self, cart: Cart, item_data: CartItemCreate) -> CartItem:
        item = CartItem(
            cart_id=cart.id,
            dish_id=item_data.dish_id,
            quantity=item_data.quantity,
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item, attribute_names=["dish"])
        return item

    async def get_items(self, cart_id: int) -> Sequence[CartItem]:
        result = await self.session.execute(
            select(CartItem)
            .options(selectinload(CartItem.dish))
            .where(CartItem.cart_id == cart_id)
        )
        return result.scalars().all()

    async def delete(self, user_id: int) -> None:
        cart = await self.get_user_cart(user_id)
        await self.session.delete(cart)
        await self.session.commit()
