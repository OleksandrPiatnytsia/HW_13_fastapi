from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=16)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactSchema(BaseModel):
    name: str = Field('Albert', min_length=3, max_length=100)
    sur_name: str = Field('Einstein', min_length=3, max_length=100)
    email: EmailStr
    phone: str = Field('+380967774411', length=13)
    birthday: date

    class Config:
        from_attributes = True


class ContactSchemaResponse(ContactSchema):
    id: int
    created_at: datetime
    updated_at: datetime
