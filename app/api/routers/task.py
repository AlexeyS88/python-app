from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.dependencies import get_task_service
from app.rabbitmq import ORDER_ROUTING_KEY, publish_json
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskNotFound, TaskService

router = APIRouter(prefix="/tasks")

@router.get("/hello-world")
def read_base_page() -> dict[str, str]:
    return {"message": "Hello World!"}

@router.get("")
def read_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return task_service.list_tasks()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreateSchema, request: Request, task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    event_data = {
        "event_id": str(uuid4()),
        "event": payload.title
    }
    await publish_json(
        exchange=request.app.state.orders_exchange,
        routing_key=ORDER_ROUTING_KEY,
        data=event_data
    )
    return task_service.create_task(task_create=payload)

@router.patch("/{task_id}")
def update_tasks(task_id: str , payload: TaskUpdateSchema, task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
        try:
            return task_service.update_task(task_id=task_id, task_update=payload)
        except TaskNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_tasks(task_id: str, task_service: TaskService = Depends(get_task_service)) -> dict[str, str]:
    try:
        task_service.delete_task(task_id=task_id)
        return {"message": f"Tasks with id={task_id} deleted"}
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")