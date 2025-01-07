from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import StreamingResponse

from app.auth import get_current_user, create_access_token, verify_password, get_password_hash
from app.database import SessionLocal, engine, Base
from app.models import URL, User
from app.crud import create_short_url, get_full_url, get_url_stats, get_me, update_user, generate_qr_code, \
    update_url_by_short_id, create_user, delete_url_by_short_id
from app.schemas import UserUpdate, URLCreate, URLUpdate, UserCreate, UserBase
from app.tasks import delete_expired_urls

Base.metadata.create_all(bind=engine)

app = FastAPI()


scheduler = BackgroundScheduler()
scheduler.add_job(
    delete_expired_urls,
    trigger=IntervalTrigger(minutes=1),
    id="delete_expired_urls",
    replace_existing=True,
    args=[SessionLocal()]
)


@app.on_event("startup")
def start_scheduler():
    scheduler.start()


@app.post("/register", response_model=UserBase)
def register_user(user_data: UserCreate):
    db = SessionLocal()
    hashed_password = get_password_hash(user_data.password)
    user_data.password = hashed_password
    user = create_user(db, user_data)
    return user


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = get_me(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user_me")
def get_user_me(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    user = get_me(db, current_user.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user


@app.patch("/user/update")
def update_current_user(user_data: UserUpdate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    user = update_user(db, user_data, current_user.id)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    return user


@app.post("/shorten")
def create_url(current_user: User = Depends(get_current_user), url_data: URLCreate = None):
    db = SessionLocal()
    short_id = create_short_url(db, url_data, current_user)
    return short_id


@app.get("/{short_id}")
def redirect_to_url(short_id: str):
    url = get_full_url(SessionLocal(), short_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url.full_url)


@app.get("/stats/{short_id}")
def get_stats(short_id: str):
    return get_url_stats(SessionLocal(), short_id)


@app.patch("/update/{short_id}")
def update_url(short_id: str, data: URLUpdate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    url = update_url_by_short_id(db, short_id, data, current_user)
    return url


@app.delete("/delete/{short_id}")
def delete_url(short_id: str, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    url = delete_url_by_short_id(db, short_id, current_user)
    return url


@app.get("/qr/{short_id}")
def get_qr_code(short_id: str):
    db = SessionLocal()
    url = db.query(URL).filter(URL.short_id == short_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    qr_buffer = generate_qr_code(short_id)
    return StreamingResponse(qr_buffer, media_type="image/png")

