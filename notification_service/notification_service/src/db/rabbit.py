from functools import lru_cache

import aio_pika
import backoff
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from aio_pika.pool import Pool
from aiormq.exceptions import AMQPConnectionError
from core import settings


@backoff.on_exception(backoff.expo, AMQPConnectionError, max_time=10)
async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbit_url)


def get_connection_pool() -> Pool[AbstractRobustConnection]:
    return Pool(get_connection, max_size=5)


async def get_channel() -> AbstractChannel:
    async with get_connection_pool().acquire() as connection:
        return await connection.channel()


@lru_cache
def get_channel_pool() -> Pool[AbstractChannel]:
    return Pool(get_channel, max_size=5)
