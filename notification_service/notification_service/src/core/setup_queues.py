import structlog
from aio_pika.abc import AbstractChannel
from aio_pika.exchange import ExchangeType
from aio_pika.pool import Pool
from core import settings

logger = structlog.get_logger()


def _make_exchange(queue_name: str) -> str:
    return queue_name + "_exchange"


async def setup(
    channel_pool: Pool[AbstractChannel],
):
    async with channel_pool.acquire() as channel:
        notify_task_exchange = await channel.declare_exchange(
            _make_exchange(settings.queue.notify_task),
            ExchangeType.FANOUT,
            auto_delete=False,
        )

        user_provided_exchange = await channel.declare_exchange(
            _make_exchange(settings.queue.user_provided),
            ExchangeType.FANOUT,
            auto_delete=False,
        )

        dlx = await channel.declare_exchange(
            _make_exchange(settings.queue.dead_letter),
            ExchangeType.FANOUT,
            auto_delete=False,
        )

        logger.info("CONFIGURED EXCHANGES")

        await channel.declare_queue(
            settings.queue.notify_task,
            auto_delete=False,
        )

        user_provided_queue = await channel.declare_queue(
            settings.queue.user_provided,
            auto_delete=False,
            arguments={
                "x-dead-letter-exchange": _make_exchange(settings.queue.dead_letter),
            },
        )

        dlx_queue = await channel.declare_queue(
            settings.queue.dead_letter,
            arguments={
                "x-dead-letter-exchange": user_provided_exchange.name,
                "x-message-ttl": settings.queue.dead_letter_ttl,
            },
            auto_delete=False,
        )

        notify_task_queue = await channel.declare_queue(
            settings.queue.notify_task,
            auto_delete=False,
        )

        await notify_task_queue.bind(notify_task_exchange.name)
        await dlx_queue.bind(dlx.name)
        await user_provided_queue.bind(user_provided_exchange.name)

    logger.info("CONFIGURED QUEUES")
