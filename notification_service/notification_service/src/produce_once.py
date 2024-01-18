import asyncio
import random
import uuid
from string import ascii_lowercase

import aio_pika
import structlog
from aio_pika.abc import AbstractChannel
from aio_pika.pool import Pool
from db.rabbit import get_channel_pool
from models import QueueMessage, QueueMessageType

logger = structlog.get_logger()


def generate_message() -> QueueMessage:
    type_ = QueueMessageType.EMAIL
    message = "".join(random.sample(ascii_lowercase, 5))
    subject = "Test subject " + "".join(random.sample(ascii_lowercase, 5))
    return QueueMessage(
        id=uuid.uuid4(),
        to_id=[],
        to_role=["user"],
        type_=type_,
        message=message,
        subject=subject,
    )


async def produce(channel_pool: Pool[AbstractChannel], exchange_name: str):
    async with channel_pool.acquire() as channel:
        logger.info("ACQUIRED PRODUCER")
        exchange = await channel.get_exchange(exchange_name)
        await exchange.publish(
            aio_pika.Message(body=generate_message().model_dump_json().encode()),
            routing_key="",
        )
        logger.info("CREATED MESSAGE")


if __name__ == "__main__":
    # queue_name = "dead_letter"
    exchange_name = "notify_task_exchange"
    channel_pool = get_channel_pool()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(produce(channel_pool, exchange_name))
