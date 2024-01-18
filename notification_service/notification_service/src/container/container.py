import structlog
from container.service_token import get_service_token
from core.logger_setup import configure_structlog
from core.settings import Settings
from db.postgres import get_user_db_connection_pool
from db.rabbit import get_channel_pool
from dependency_injector import containers, providers
from services.notification_provider import SMTPProvider, TestProvider
from services.task_status_service import TaskStatusService
from services.user_provider import UserProvider


class Container(containers.DeclarativeContainer):
    settings: providers.Singleton[Settings] = providers.Singleton(Settings)

    postgres_connection_pool: providers.Factory = providers.Factory(get_user_db_connection_pool)
    rabbit_channel_pool: providers.Singleton = providers.Singleton(get_channel_pool)

    logging: providers.Resource = providers.Resource(
        configure_structlog,
        settings().json_logging_level,
        settings().console_logging_level,
    )

    tokens: providers.Resource = providers.Resource(get_service_token)

    smtp_provider: providers.Singleton[SMTPProvider] = providers.Singleton(
        SMTPProvider,
        smtp_host=settings().smtp.host,
        smtp_port=settings().smtp.port,
        login=settings().smtp.login,
        password=settings().smtp.password,
        logger=structlog.get_logger("smtp_provider"),
    )

    test_provider: providers.Singleton[TestProvider] = providers.Singleton(
        TestProvider,
        logger=structlog.get_logger("test_provider"),
    )

    user_provider: providers.Singleton[UserProvider] = providers.Singleton(
        UserProvider,
        logger=structlog.get_logger("user_provider"),
        connection_pool=postgres_connection_pool,
        tokens=tokens,
    )

    task_status_service: providers.Singleton[TaskStatusService] = providers.Singleton(
        TaskStatusService,
        connection_pool=postgres_connection_pool,
        table_name=settings().notify_db.notify_status_table_name,
        logger=structlog.get_logger("task_status"),
    )
