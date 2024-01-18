import asyncpg
import backoff
from core import settings


@backoff.on_exception(backoff.expo, Exception, max_time=60)
async def get_notify_db_connection_pool():
    pool = await asyncpg.create_pool(settings.notify_db_dsn)
    return pool


@backoff.on_exception(backoff.expo, Exception, max_time=60)
async def get_user_db_connection_pool():
    pool = await asyncpg.create_pool(settings.user_db_dsn)
    return pool
