from typing import Optional

import asyncpg
import backoff
from asyncpg import Pool
from asyncpg.exceptions import InterfaceError, PostgresConnectionError


connection: Optional[Pool] = None


@backoff.on_exception(backoff.expo, [PostgresConnectionError, InterfaceError], max_time=60)
async def get_connection_pool(dsn):
    pool = await asyncpg.create_pool(dsn)
    return pool


def get_connection():
    return connection
