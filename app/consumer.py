import asyncio
import json
import os
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from dotenv import load_dotenv
from rabbitmq import connect_rabbitmq, declare_notification_queue, declare_orders_exchange

load_dotenv()

async def handle_order_created(message: AbstractIncomingMessage):
    event_data = json.loads(message.body.decode())
    print(f"Получено сообщение:", event_data)
    await message.ack()

async def main():
    rmq_user = os.environ["RABBITMQ_DEFAULT_USER"]
    rmq_pass = os.environ["RABBITMQ_DEFAULT_PASS"]
    rmq_host = os.getenv("RABBITMQ_DEFAULT_HOST", "localhost")
    
    url = f"amqp://{rmq_user}:{rmq_pass}@{rmq_host}:5672/"

    connection = await aio_pika.connect_robust(url=url)
    channel = await connection.channel()
    orders_exchange = await declare_orders_exchange(channel)
    queue = await declare_notification_queue(channel, orders_exchange)
    await queue.consume(handle_order_created)
    try:
        await asyncio.Future()
    finally:
        print("Закрытие соединения")
        await connection.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа успешно остановлена")