from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.conf.config import config
from src.services.auth import auth_service

conf = ConnectionConfig(
    MAIL_USERNAME=config.mail_username,
    MAIL_PASSWORD=config.mail_password,
    MAIL_FROM=config.mail_username,
    MAIL_PORT=config.mail_port,
    MAIL_SERVER=config.mail_server,
    MAIL_FROM_NAME=config.mail_sender_name,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def simple_send_mail(email: EmailStr, email_text:str) -> object:
    """
    The simple_send_mail function sends an email to the specified recipient.
        Args:
            email (str): The recipient's email address.
            text (str): The body of the message to be sent.

    :param email: EmailStr: Specify the email address to send the message to
    :param email_text:str: Pass the text of the email to be sent
    :return: The object, which is the message that was sent
    """
    message = MessageSchema(
        subject="Fastapi-Mail test",
        recipients=[email],
        # body="Test fast api mail",
        body =email_text,
        subtype=MessageType.plain)

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_email(email: EmailStr, username: str, host: str):

    """
    The send_email function sends an email to the user with a link to confirm their email address.
        Args:
            email (str): The user's email address.
            username (str): The username of the user who is registering for an account.  This will be used in the message body of the confirmation message sent to them via FastMail.

    :param email: EmailStr: Specify the email address of the recipient
    :param username: str: Personalize the email message
    :param host: str: Pass the hostname of your application to the template
    :return: A coroutine object
    """
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
