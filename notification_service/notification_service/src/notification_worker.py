import asyncio

import services.consumer as consumer
from container import setup
from core import settings
from resolver.type_resolver import resolver


async def run():
    task = asyncio.create_task(
        consumer.consumer(
            callback=resolver,
            queue_name=settings.queue.user_provided,
        ),
    )

    await task


def main():
    setup()
    asyncio.run(run())


if __name__ == "__main__":
    main()
