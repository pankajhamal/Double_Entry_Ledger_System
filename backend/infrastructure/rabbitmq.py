import aio_pika
from aio_pika import Channel, Connection

from backend.core.config import settings

class RabbitMQ:
    def __init__(self):
        self.connection: Connection | None = None
        self.channel: Channel | None = None

    async def connect(self):
        url = (
            f"amqp://{settings.RABBITMQ_DEFAULT_USER}:"
            f"{settings.RABBITMQ_DEFAULT_PASSWORD}@"
            f"{settings.RABBITMQ_HOST}:"
            f"{settings.RABBITMQ_PORT}/"
        )

        self.connection = await aio_pika.connect_robust(url)
        self.channel = await self.connection.channel()

        await self.channel.declare_queue(
            settings.RABBITMQ_QUEUE,
            durable=True,
        )

    async def close(self):
        if self.connection:
            await self.connection.close()


rabbitmq = RabbitMQ()