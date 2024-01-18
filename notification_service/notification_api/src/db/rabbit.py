from typing import Optional

import aio_pika
import backoff
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractRobustConnection
from aiormq.exceptions import AMQPConnectionError

rabbitmq_client: Optional[AbstractConnection] = None
rabbitmq_channel: Optional[AbstractChannel] = None


@backoff.on_exception(backoff.expo, AMQPConnectionError, max_time=30)
async def get_connection(dsn) -> AbstractRobustConnection:
    return await aio_pika.connect_robust(dsn)


def get_channel():
    return rabbitmq_channel
