from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.task import TaskService
from app.core.config import settings


def get_task_service(db: Session = Depends(get_db)):
    return TaskService(
        db=db,
        cache_redis_url=settings.redis_url,
        cache_ttl_seconds=settings.cache_ttl_seconds,
        cache_task_key=settings.cache_task_key
    )