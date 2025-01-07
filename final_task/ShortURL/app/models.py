from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    short_id = Column(String, unique=True, index=True)
    full_url = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    creator = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="urls")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    urls = relationship("URL", back_populates="user")

