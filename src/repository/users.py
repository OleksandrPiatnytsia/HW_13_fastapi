import logging

from libgravatar import Gravatar
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.db import get_db

from src.database.models import User
from src.schemas import UserSchema

from fastapi import Depends


def get_user_by_email(email: str, session) -> User:
    sq = select(User).filter_by(email=email)
    result = session.execute(sq)
    user = result.scalar_one_or_none()
    # logging.error(f"!!!!!!!!!!!!!!USER!!!!!!!!!!!!!!!!   {user}")
    return user


def create_user(body: UserSchema, session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        logging.error(e)

    new_user = User(**body.model_dump(), avatar=avatar)  # User(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def update_token(user: User, token: str | None, session) -> None:
    user.refresh_token = token
    session.commit()