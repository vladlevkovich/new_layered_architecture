from datetime import datetime, timedelta, timezone

from app.src.core import scheduler
from app.src.repository import OrderRepository
from app.src.schemas.order_shema import OrderCreateResponse, OrderSchema

from .notification_service import NotificationService


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        notification_service: NotificationService,
    ):
        self.order_repository = order_repository
        self.notification_service = notification_service

    async def create_order(self, user_id: int, user_email: str) -> OrderCreateResponse:
        order = await self.order_repository.create_order(user_id)
        await self.scheduled_send_email(order.id, user_email)
        return OrderCreateResponse(
            id=order.id,
            user_id=order.user_id,
            delivery_time=order.delivery_time,
            is_ready=order.is_ready,
            is_notified=order.is_notified,
            created_at=order.created_at,
        )

    async def scheduled_send_email(self, order_id: int, user_email: str) -> None:
        # scheduler = AsyncIOScheduler()
        # scheduler.start()
        run_time = datetime.now(timezone.utc) + timedelta(minutes=1)

        async def job() -> None:
            await self.notification_service.send_order_ready_notification(
                user_email, order_id
            )

        scheduler.add_job(
            job,
            trigger="date",
            next_run_time=run_time,
            # args=[order_id, user_email],
            id=f"order_email_{order_id}",
            replace_existing=True,
        )

    async def get_order_detail(self, user_id: int) -> OrderSchema:
        order = await self.order_repository.get_order_detail(user_id)
        return OrderSchema.model_validate(order)
