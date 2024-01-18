from typing import Any

import structlog
from core.settings import settings
from db.postgres import Pool, get_connection
from errors.template import TemplateNotFound
from fastapi import Depends
from schemas.task import TemplateSchema


class TemplateService:
    def __init__(
        self,
        con_pool: Pool,
        logger: Any,
    ):
        self.con_pool = con_pool
        self.logger = logger

    async def get_template_by_slug(self, slug) -> TemplateSchema:
        async with self.con_pool.acquire() as con:
            table_name = settings.postgres_table.get_table_name(settings.postgres_table.template)
            result = await con.fetchrow(f"SELECT * FROM {table_name} WHERE slug = $1;", slug)  # noqa: S608
            if not result:
                raise TemplateNotFound
            self.logger.info("Got template", slug=slug)
            return TemplateSchema(**result)


def get_template_service(con_pool: Pool = Depends(get_connection)):
    return TemplateService(
        con_pool,
        logger=structlog.get_logger(),
    )
