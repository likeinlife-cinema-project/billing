import uuid

import structlog
from fastapi import Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from structlog.stdlib import BoundLogger

from auth_app.db.sqlalchemy import get_async_session
from auth_app.errors.external import RoleAlreadyExists, RoleNotFound
from auth_app.models.domain import Role


class RoleRepository:
    def __init__(self, session: AsyncSession, logger: BoundLogger) -> None:
        self.session = session
        self.logger = logger

    async def create(
        self,
        name: str,
        description: str,
    ) -> Role:
        """Create a role."""
        role = Role(name=name, description=description)
        try:
            self.session.add(role)
            await self.session.commit()
            await self.session.refresh(role)
            self.logger.info("Create", role_id=role.id)
        except IntegrityError:
            self.logger.warning("Already exists", name=name)
            raise RoleAlreadyExists(name)
        return role

    async def get(self, role_id: uuid.UUID) -> Role:
        result = await self.session.execute(select(Role).where(Role.id == role_id))
        try:
            self.logger.info("Get", role_id=role_id)
            return result.scalar_one()
        except NoResultFound:
            self.logger.info("Not exists", role_id=role_id)
            raise RoleNotFound(role_id)

    async def get_by_name(self, role_name: str) -> Role:
        result = await self.session.execute(select(Role).where(Role.name == role_name))
        try:
            return result.scalar_one()
        except NoResultFound:
            raise RoleNotFound(role_name)

    async def get_list(self, limit: int, offset: int) -> list[Role]:
        result = await self.session.execute(
            select(Role).order_by(Role.name.asc()).limit(limit).offset(offset),
        )
        return result.scalars().all()

    async def delete(self, role_id: uuid.UUID) -> bool:
        result = await self.session.execute(delete(Role).where(Role.id == role_id).returning(Role.id))
        try:
            deleted_id = result.scalar_one()
        except NoResultFound:
            raise RoleNotFound(role_id)

        await self.session.commit()
        if deleted_id:
            self.logger.info("Delete", role_id=role_id)
            return True
        self.logger.warning("Cant delete", role_id=role_id)
        return False

    async def update(
        self,
        role_id: uuid.UUID,
        name: str | None = None,
        description: str | None = None,
    ) -> Role:
        statement = select(Role).where(Role.id == role_id)
        result = await self.session.execute(statement)
        try:
            role = result.scalar_one()
        except NoResultFound:
            raise RoleNotFound(role_id)
        if name:
            role.name = name
        if description:
            role.description = description

        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)
        self.logger.info("Update", role_id=role.id)
        return role


async def get_role_repository(session: AsyncSession = Depends(get_async_session)) -> RoleRepository:
    logger = structlog.get_logger()
    return RoleRepository(session=session, logger=logger)
