from sqlalchemy import ScalarResult, select
from sqlalchemy.orm import Session
from app.models.task import TaskOrm


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> ScalarResult[TaskOrm]:
        return self.db.scalars(select(TaskOrm))

    def get_by_id(self, task_id: str) -> TaskOrm | None:
        return self.db.get(TaskOrm, task_id)

    def create(self, title: str) -> TaskOrm:
        new_task = TaskOrm(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    def delete(self, task: TaskOrm) -> TaskOrm:
        self.db.delete(task)
        return task