from contextlib import asynccontextmanager
from uuid import uuid4

import uvicorn
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    print('Таблицы созданы')
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*']
)

DATABASE_URL = 'postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres'
engine = create_engine(
    url=DATABASE_URL
)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4)
    )


class TaskModel(Base):
    __tablename__ = 'tasks'
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoryModel(Base):
    __tablename__ = 'categories'
    name: Mapped[str]


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str | None = None


tasks: list[TaskSchema] = []

categories: list[CategorySchema] = []


def task_orm_to_model(task_orm):
    return TaskSchema(
        id=task_orm.id,
        title=task_orm.title,
        completed=task_orm.completed
        )


def category_orm_to_model(category_orm):
    return CategorySchema(
        id=category_orm.id,
        name=category_orm.name
        )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/tasks')
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.scalars(select(TaskModel)).all()
    return [task_orm_to_model(task) for task in tasks]


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_tasks(payload: TaskCreateSchema, db: Session = Depends(get_db)):
    new_task = TaskModel(
        title=payload.title,
        completed=False
    )
    db.add(new_task)
    db.commit()
    return new_task


@app.patch('/tasks/{task_id}')
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    db: Session = Depends(get_db)
):
    task = db.get(TaskModel, task_id)
    if payload.title:
        task.title = payload.title
    if payload.completed is not None:
        task.completed = payload.completed

    db.commit()

    return task


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.get(TaskModel, task_id)
    db.delete(task)
    db.commit()


@app.get('/categories')
def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    categories = db.scalars(select(CategoryModel)).all()
    return [category_orm_to_model(category) for category in categories]


@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    new_cotegory = CategoryModel(
        name=payload.name
    )
    db.add(new_cotegory)
    db.commit()
    return new_cotegory


@app.patch('/categories/{category_id}')
def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.get(CategoryModel, category_id)
    if payload.name:
        category.name = payload.name
    db.commit()
    return category


@app.delete(
        '/categories/{category_id}',
        status_code=status.HTTP_204_NO_CONTENT
    )
def delete_category(category_id: str, db: Session = Depends(get_db)):
    category = db.get(CategoryModel, category_id)
    db.delete(category)
    db.commit()


if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, reload=True)
