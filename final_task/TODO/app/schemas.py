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


class TodoBase(BaseModel):
    title: str = Field(..., max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None
