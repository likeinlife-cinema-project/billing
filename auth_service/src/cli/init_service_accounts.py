import asyncio

import typer
from auth_app.core.config import settings
from auth_app.errors.external import RoleAlreadyExists
from pydantic import BaseModel, TypeAdapter

from .admin import get_role_service, get_user_role_service, get_user_service

router = typer.Typer(help="Commands with auth service")


class ServiceAccount(BaseModel):
    email: str
    password: str


async def _init_service_accounts() -> None:
    file_path = settings.service_account_settings.file_path
    if not file_path:
        print("No service accounts file provided")
        return

    with open(file_path, "r") as file_obj:
        accounts = TypeAdapter(list[ServiceAccount]).validate_json(file_obj.read())
        print("Service accounts file provided. Creating")

    async with get_role_service() as service:
        try:
            await service.create("service", "Service role")
        except RoleAlreadyExists:
            await service.role_repository.session.rollback()

        service_role = await service.get_by_name("service")

    for account_info in accounts:
        async with get_user_service() as service:
            service_account = await service.create(email=account_info.email, password=account_info.password)

        async with get_user_role_service() as service:
            await service.set_user_role(service_account.id, service_role.id)

            print("Service account {account_info.email} created")


@router.command(help="Init service accounts")
def init_service_accounts() -> None:
    asyncio.run(_init_service_accounts())
