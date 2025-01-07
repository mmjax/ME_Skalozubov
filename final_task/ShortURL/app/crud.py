import string
import qrcode
import random
from io import BytesIO

from starlette import status
from starlette.responses import JSONResponse

from app.models import URL, User
from fastapi import HTTPException

from app.schemas import UserCreate, UserUpdate, URLUpdate


def create_user(db, user_data: UserCreate):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exists"
        )
    user = User(
        username=user_data.username,
        password=user_data.password,
        email=user_data.email,
        full_name=user_data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db, user_data: UserUpdate, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.full_name:
        user.full_name = user_data.full_name

    db.commit()
    db.refresh(user)

    return user


def get_me(db, username):
    return db.query(User).filter(User.username == username).first()


def create_short_url(db, url_data, creator):
    short_id = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    new_url = URL(
        full_url=url_data.full_url,
        short_id=short_id,
        expires_at=url_data.expires_at,
        creator=creator.id
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return {"short_url": short_id}


def update_url_by_short_id(db, short_id, data: URLUpdate, current_user: User):
    url = get_full_url(db, short_id)
    if not url:
        raise HTTPException(status_code=404, detail="Todo not found")
    if url.creator != current_user.id:
        raise HTTPException(status_code=404, detail="Only creator can change this url")
    if data.full_url:
        url.full_url = data.full_url
    if data.expires_at:
        url.expires_at = data.expires_at
    db.commit()
    db.refresh(url)
    return url


def get_full_url(db, short_id):
    return db.query(URL).filter(URL.short_id == short_id).first()


def get_url_stats(db, short_id):
    url = get_full_url(db, short_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url


def generate_qr_code(short_url: str):
    qr = qrcode.make(short_url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def delete_url_by_short_id(db, short_id, current_user):
    url = get_full_url(db, short_id)
    if not url:
        raise HTTPException(status_code=404, detail="Todo not found")
    if url.creator != current_user.id:
        raise HTTPException(status_code=404, detail="Only creator can delete this url")
    db.delete(url)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
