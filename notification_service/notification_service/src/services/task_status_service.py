import datetime
from typing import Any

from asyncpg import Connection
from asyncpg.pool import Pool
from models.notification_status import NotifyStatus


class TaskStatusService:
    def __init__(
        self,
        connection_pool: Pool,
        table_name: str,
        logger: Any,
    ):
        self.connection_pool = connection_pool
        self.table_name = table_name
        self.logger = logger

    async def upsert(self, notify: NotifyStatus) -> None:
        con: Connection
        async with self.connection_pool.acquire() as con:
            query = (
                f"INSERT INTO {self.table_name} (id, task_id, subject, status, description, notification_type) "  # noqa: S608
                "VALUES ($1, $2, $3, $4, $5, $7) "
                "ON CONFLICT (id) "
                "DO UPDATE SET status=$4, description=$5, updated_at=$6 "
                "RETURNING id;"
            )
            result = await con.fetch(
                query,
                notify.id,
                notify.task_id,
                notify.subject,
                notify.status,
                notify.description,
                datetime.datetime.now(),
                notify.type,
            )

            if not result:
                self.logger.error(
                    "Cant upsert task status",
                    task_id=notify.task_id,
                    id=notify.id,
                    status=notify.status,
                    description=notify.description,
                    result=result,
                )
            self.logger.info(
                "Upsert task status",
                task_id=notify.task_id,
                id=notify.id,
                status=notify.status,
                description=notify.description,
            )
