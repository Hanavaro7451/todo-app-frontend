from sqlalchemy.orm import Session

from repositories.task import TaskRepository
from schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from services.exceptions import NotFound


class TaskService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repo = TaskRepository(db)

    def list_task(self) -> list[TaskSchema]:
        tasks = self.task_repo.get_all()
        return [
            TaskSchema.model_validate(task) for task in tasks
        ]

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task = self.task_repo.create_task(title=task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task)

    def update_task(self, task_id, task_update: TaskUpdateSchema
                    ) -> TaskSchema:
        task_for_update = self.task_repo.get_by_id(task_id)
        if task_for_update is None:
            raise NotFound('Задача не найдена')
        if task_update.title:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        return TaskSchema.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repo.get_by_id(task_id)
        if task_for_delete is None:
            raise NotFound('Задача не найдена')
        self.task_repo.delete_task(task_for_delete)
