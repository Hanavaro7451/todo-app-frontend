from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services.category import CategoryService
from services.task import TaskService


def get_task_service(db: Session = Depends(get_db)):
    return TaskService(db)


def get_category_services(db: Session = Depends(get_db)):
    return CategoryService(db)
