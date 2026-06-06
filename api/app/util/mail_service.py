from pydantic import EmailStr
from fastapi_mail import FastMail, MessageSchema, MessageType

# config
from config.email_config import mail_conf


class MailService:
    @staticmethod
    async def send_mail(
        correo: EmailStr,
        asunto: str,
        template_name: str,
        context: dict | None = None,
    ):

        message = MessageSchema(
            subject=asunto,
            recipients=[correo],
            template_body=context or {},
            subtype=MessageType.html,
        )

        fm = FastMail(mail_conf)
        await fm.send_message(message, template_name=template_name)
