from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(...)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=100)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)


class URLCreate(BaseModel):
    full_url: str
    expires_at: Optional[datetime] = Field(None)


class URLUpdate(BaseModel):
    full_url: Optional[str] = Field(None)
    expires_at: Optional[datetime] = Field(None)
