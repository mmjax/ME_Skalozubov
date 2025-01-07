from starlette import status
from starlette.responses import JSONResponse

from app.models import Todo, User
from fastapi import HTTPException

from app.schemas import UserCreate, UserUpdate, TodoCreate, TodoUpdate


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


def create_todo(db, todo_data: TodoCreate, current_user: User):
    todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        completed=todo_data.completed,
        user_id=current_user.id
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_my_todos(db, current_user):
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()


def get_todo(db, todo_id, current_user):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()


def update_todo(db, todo_id, todo_data: TodoUpdate, current_user: User):
    todo = get_todo(db, todo_id, current_user)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo_data.title:
        todo.title = todo_data.title
    if todo_data.description:
        todo.description = todo_data.description
    if todo_data.completed:
        todo.completed = todo_data.completed
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db, todo_id, current_user):
    todo = get_todo(db, todo_id, current_user)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
