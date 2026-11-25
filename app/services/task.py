import json
from typing import cast

from sqlalchemy.orm import Session

from app.cache.redis import RedisCacheBackend
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema


class TaskNotFound(Exception):
    """Task not found"""

class TaskService:
    def __init__(self, db: Session, cache_redis_url: str, cache_ttl_seconds: int, cache_task_key: str) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)
        self.cache = RedisCacheBackend(cache_redis_url, cache_ttl_seconds)
        self.cache_task_key = cache_task_key

    def list_tasks(self) -> list[TaskSchema]:
        cached_tasks = self.cache.get(self.cache_task_key)
        print("DEBUG TYPE:", type(cached_tasks), "DEBUG VALUE:", cached_tasks)
        if cached_tasks is not None:
            cached_tasks = cast(list[dict], cached_tasks)
            return [TaskSchema.model_validate(task) for task in cached_tasks]

        tasks_orm = self.task_repository.get_all()
        task_read = [TaskSchema.model_validate(task) for task in tasks_orm]
        task_for_cache = [task.model_dump() for task in task_read]
        self.cache.set(self.cache_task_key, json.dumps(task_for_cache))
        return task_read

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        self.cache.delete(self.cache_task_key)
        task_orm = self.task_repository.create(title=task_create.title)
        self.db.commit()
        self.db.refresh(task_orm)
        return TaskSchema.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        self.cache.delete(self.cache_task_key)
        
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        
        if task_for_update:
            if task_update.title:
                task_for_update.title = task_update.title
            if task_update.completed:
                task_for_update.completed = task_update.completed
            self.db.commit()
            self.db.refresh(task_for_update)
            return TaskSchema.model_validate(task_for_update)
        
        raise TaskNotFound(f"Task with id={task_id} not found")
        

    def delete_task(self, task_id: str) -> TaskSchema:
        self.cache.delete(self.cache_task_key)

        task_for_delete = self.task_repository.get_by_id(task_id=task_id)

        if task_for_delete:
            self.task_repository.delete(task_for_delete)
            self.db.commit()
            return TaskSchema.model_validate(task_for_delete)
        
        raise TaskNotFound(f"Task with id={task_id} not found")
        