from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.task import TaskModel


class TaskRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> Sequence[TaskModel]:
        return self.db.scalars(select(TaskModel)).all()

    def get_by_id(self, task_id: str) -> TaskModel | None:
        return self.db.get(TaskModel, task_id)

    def create_task(self, title: str) -> TaskModel | None:
        new_task = TaskModel(title=title, completed=False)
        self.db.add(new_task)
        self.db.commit()
        return new_task

    def delete_task(self, TaskModel) -> None:
        self.db.delete(TaskModel)
        self.db.commit()
