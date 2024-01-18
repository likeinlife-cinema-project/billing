import asyncio

from core.setup_queues import setup
from db.rabbit import get_channel_pool


async def main():
    channel_pool = get_channel_pool()
    await setup(channel_pool)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())
