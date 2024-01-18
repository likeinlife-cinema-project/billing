from typing import Any
from uuid import UUID

import structlog
from asyncpg import Connection
from core.settings import settings
from db.postgres import Pool, get_connection
from errors.notification import NotificationNotFound
from fastapi import Depends
from schemas.notification import NotifyStatusSchema


class TaskStatusService:
    def __init__(
        self,
        con_pool: Pool,
        table_name: str,
        logger: Any,
    ):
        self.con_pool = con_pool
        self.table_name = table_name
        self.logger = logger

    async def by_id(self, id_: UUID) -> list[NotifyStatusSchema]:
        con: Connection
        async with self.con_pool.acquire() as con:
            result = await con.fetch(f"SELECT * FROM {self.table_name} WHERE task_id = $1;", id_)  # noqa: S608
            if not result:
                raise NotificationNotFound
            self.logger.info("Got task status", id=id_)
            return [NotifyStatusSchema(**i) for i in result]


def get_task_status_service(
    con_pool: Pool = Depends(get_connection),
) -> TaskStatusService:
    table_name = settings.postgres_table.get_table_name(settings.postgres_table.notification_status)
    return TaskStatusService(
        con_pool=con_pool,
        table_name=table_name,
        logger=structlog.get_logger(),
    )
