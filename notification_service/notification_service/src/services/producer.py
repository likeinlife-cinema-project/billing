import aio_pika
import structlog
from aio_pika.abc import AbstractChannel
from aio_pika.pool import Pool
from container import Container
from dependency_injector.wiring import Provide, inject

logger = structlog.get_logger()


@inject
async def produce(
    exchange_name: str,
    message: bytes,
    channel_pool: Pool[AbstractChannel] = Provide[Container.rabbit_channel_pool],
):
    async with channel_pool.acquire() as channel:
        exchange = await channel.get_exchange(exchange_name)
        await exchange.publish(
            aio_pika.Message(body=message),
            routing_key="",
        )

        logger.info("PRODUCED MESSAGE")
