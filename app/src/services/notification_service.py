from .email_service import EmailService


class NotificationService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    async def send_order_ready_notification(
        self, user_email: str, order_id: int
    ) -> bool:
        """
        Sends a message that the order is ready
        """
        return await self.email_service.send_order_ready_notification(
            user_email, order_id
        )
