from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.schemas import UserResponseSchema
from src.services.auth import auth_service
from src.services.avatar import UploadService

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory='templates')


@router.get("/me/", response_model=UserResponseSchema)
def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.patch('/avatar', response_model=UserResponseSchema)
def update_avatar_user(avatar: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                       session: Session = Depends(get_db)):
    public_id = UploadService.create_name_avatar(current_user.email, current_user.username)

    r = UploadService.upload(avatar.file, public_id)

    src_url = UploadService.get_url_avatar(public_id, r.get('version'))
    user = repository_users.update_avatar(current_user.email, src_url, session)
    return user
