from fastapi import FastAPI, HTTPException, Depends
from app.database import SessionLocal, engine, Base
from app.models import User
from app.auth import get_password_hash, get_current_user
from app.crud import create_todo, get_my_todos, get_todo, update_todo, delete_todo, get_me, create_user, \
    get_me, update_user
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import verify_password, create_access_token

from app.schemas import UserBase, UserCreate, UserUpdate, TodoCreate, TodoUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/register", response_model=UserBase)
def register_user(user_data: UserCreate):
    db = SessionLocal()
    if get_me(db, user_data.username):
        raise HTTPException(status_code=400, detail="User already exists")
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


@app.post("/items")
def create_item(item_data: TodoCreate, current_user: User = Depends(get_current_user)):
    return create_todo(SessionLocal(), item_data, current_user)


@app.get("/items")
def read_items(current_user: User = Depends(get_current_user)):
    return get_my_todos(SessionLocal(), current_user)


@app.get("/items/{item_id}")
def read_item(item_id: int, current_user: User = Depends(get_current_user)):
    return get_todo(SessionLocal(), item_id, current_user)


@app.put("/items/{item_id}")
def update_item(
        item_id: int,
        item_data: TodoUpdate,
        current_user: User = Depends(get_current_user)
):
    return update_todo(SessionLocal(), item_id, item_data, current_user)


@app.delete("/items/{item_id}")
def delete_item(item_id: int, current_user: User = Depends(get_current_user)):
    return delete_todo(SessionLocal(), item_id, current_user)
