import json
import os
import aio_pika

from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue
from dotenv import load_dotenv

NOTIFICATIONS_QUEUE = "notification.order_created"
ORDER_EXCHANGE = "order"
ORDER_ROUTING_KEY = "order.created"

load_dotenv()
async def connect_rabbitmq():
    rmq_user = os.environ["RABBITMQ_DEFAULT_USER"]
    rmq_pass = os.environ["RABBITMQ_DEFAULT_PASS"]
    rmq_host = os.getenv("RABBITMQ_DEFAULT_HOST", "localhost")

    url = f"amqp://{rmq_user}:{rmq_pass}@{rmq_host}:5672/"
    return await aio_pika.connect_robust(url=url)

async def declare_orders_exchange(channel: AbstractChannel):
    return await channel.declare_exchange(ORDER_EXCHANGE)

async def declare_notification_queue(channel: AbstractChannel, exchange: AbstractExchange):
    queue: AbstractQueue = await channel.declare_queue(NOTIFICATIONS_QUEUE, durable=True)
    await queue.bind(exchange, routing_key=ORDER_ROUTING_KEY)
    return queue

async def publish_json(exchange: AbstractExchange, routing_key: str, data: dict):
    message = aio_pika.Message(json.dumps(data).encode())
    await exchange.publish(message, routing_key)