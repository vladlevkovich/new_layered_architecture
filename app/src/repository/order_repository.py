from datetime import datetime, timedelta, timezone
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.src.models import Cart, CartItem, Order, OrderItem
from app.src.repository import CartRepository
from app.src.schemas.report_schema import OrderItemReport, OrderReport
from app.src.schemas.user_schema import UserResponse


class OrderRepository:
    def __init__(self, session: AsyncSession, cart_repository: CartRepository):
        self.session = session
        self.cart_repository = cart_repository

    async def get_order(self, user_id: int) -> Order | None:
        order = await self.session.execute(
            select(Order).where(Order.user_id == user_id)
        )
        return order.scalars().first()

    async def create_order(self, user_id: int) -> Order:
        order = Order(
            user_id=user_id,
            delivery_time=datetime.now(timezone.utc) + timedelta(minutes=30),
        )
        self.session.add(order)
        await self.session.commit()
        await self.create_order_item(order.id, user_id)
        return order

    async def create_order_item(self, order_id: int, user_id: int) -> None:
        cart_result = await self.session.execute(
            select(Cart)
            .options(selectinload(Cart.items).selectinload(CartItem.dish))
            .where(Cart.user_id == user_id)
        )
        cart = cart_result.scalars().first()

        if not cart:
            return

        order_items = [
            OrderItem(order_id=order_id, dish_id=item.dish_id, quantity=item.quantity)
            for item in cart.items
        ]
        self.session.add_all(order_items)
        await self.session.commit()
        await self.cart_repository.delete(user_id)

    async def get_order_detail(self, user_id: int) -> Order | None:
        order = await self.get_order(user_id)
        if order is None:
            raise ValueError("Order not found")

        order_item = await self.session.execute(
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.dish))
            .where(Order.id == order.id)
        )
        return order_item.scalars().first()

    async def get_all_orders_with_details(self) -> List[OrderReport]:
        one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)
        result = await self.session.execute(
            select(Order)
            .where(Order.created_at >= one_month_ago)
            .options(
                selectinload(Order.user),
                selectinload(Order.items).selectinload(OrderItem.dish),
            )
        )
        return [
            OrderReport(
                id=order.id,
                user=UserResponse(
                    id=order.user.id,
                    email=order.user.email,
                    first_name=order.user.first_name,
                    last_name=order.user.last_name,
                ),
                delivery_time=order.delivery_time,
                created_at=order.created_at,
                is_ready=order.is_ready,
                items=[
                    OrderItemReport(
                        dish_name=item.dish.name,
                        quantity=item.quantity,
                        price=item.dish.price,
                    )
                    for item in order.items
                ],
            )
            for order in result.scalars().all()
        ]
