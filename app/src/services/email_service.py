from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

import aiosmtplib


class EmailService:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None,
    ) -> bool:
        try:
            msg = MIMEMultipart()
            msg["From"] = from_email or self.smtp_user
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            await aiosmtplib.send(
                msg,
                hostname=self.smtp_host,
                port=self.smtp_port,
                start_tls=True,
                username=self.smtp_user,
                password=self.smtp_password,
            )

            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    async def send_order_ready_notification(
        self, user_email: str, order_id: int
    ) -> bool:
        subject = "Ваше замовлення готове!"
        body = f"""
        Замовлення #{order_id} вже готове до отримання.
        """
        return await self.send_email(user_email, subject, body)
