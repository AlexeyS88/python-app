from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.api.routers.task import router as task_router

from contextlib import asynccontextmanager
from app.core.config import settings
from app.models.base import Base
from app.db.session import engine
from app.rabbitmq import connect_rabbitmq, declare_notification_queue, declare_orders_exchange

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск приложения")
    Base.metadata.create_all(bind=engine)
    connection = await connect_rabbitmq()
    channel = await connection.channel()
    orders_exchange = await declare_orders_exchange(channel)
    app.state.orders_exchange = orders_exchange
    yield 
    await connection.close()
    print("Выключение приложения")

app = FastAPI(lifespan=lifespan)
app.include_router(task_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origin,
    allow_methods=["*"],
    allow_headers=["*"]
)


    