from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.database.db import email_password, email_sender
from src.services.auth import auth_service

conf = ConnectionConfig(
    MAIL_USERNAME=email_sender,
    MAIL_PASSWORD=email_password,
    MAIL_FROM=email_sender,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def simple_send_mail(email: EmailStr):
    message = MessageSchema(
        subject="Fastapi-Mail test",
        recipients=[email],
        body="Test fast api mail",
        subtype=MessageType.plain)

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_email(email: EmailStr, username: str, host: str):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
        print(f"mail sended to email: {email}")
    except ConnectionErrors as err:
        print(err)
