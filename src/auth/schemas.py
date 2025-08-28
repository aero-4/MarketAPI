from typing import Optional, Any

from pydantic import BaseModel, EmailStr


class SentCodeSchema(BaseModel):
    phone: int


class LoginSchema(BaseModel):
    code: int
    phone: int


class SentEmailSchema(BaseModel):
    email: EmailStr


class UserSchema(BaseModel):
    id: Optional[int] = None
    date_at: Any = None
    role: int = None

    first_name: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    photo: Optional[str] = None
    phone: Optional[int] = None
    balance: Optional[int] = None


class TokensInfo(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
