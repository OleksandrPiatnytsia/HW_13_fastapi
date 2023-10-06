from fastapi import APIRouter, HTTPException, Depends, status, Security, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.schemas import UserSchema, UserResponseSchema, TokenModel, MailSchema
from src.services.auth import auth_service
from src.services.email import send_email, simple_send_mail

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/send_mail_test", status_code=status.HTTP_201_CREATED)
def send_mail_test(body: MailSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(simple_send_mail, body.email)


@router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def signup(body: UserSchema, background_tasks: BackgroundTasks, request: Request, session: Session = Depends(get_db)):
    exist_user = repository_users.get_user_by_email(body.email, session)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = repository_users.create_user(body, session)
    background_tasks.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post("/login", response_model=TokenModel)
def login(body: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    user = repository_users.get_user_by_email(body.username, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    # Generate JWT
    access_token = auth_service.create_access_token(data={"sub": user.email})
    refresh_token = auth_service.create_refresh_token(data={"sub": user.email})

    repository_users.update_token(user, refresh_token, session)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security),
                  session: Session = Depends(get_db)):
    token = credentials.credentials
    email = auth_service.decode_refresh_token(token)
    user = repository_users.get_user_by_email(email, session)

    if user.refresh_token != token:
        repository_users.update_token(user, None, session)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = auth_service.create_access_token(data={"sub": email})
    refresh_token = auth_service.create_refresh_token(data={"sub": email})
    repository_users.update_token(user, refresh_token, session)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
def confirmed_email(token: str, session: Session = Depends(get_db)):
    email = auth_service.get_email_from_token(token)
    user = repository_users.get_user_by_email(email, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    repository_users.confirmed_email(email, session)
    return {"message": "Email confirmed"}
