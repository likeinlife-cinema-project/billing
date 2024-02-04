import uuid
from contextlib import asynccontextmanager

import structlog
from api import healthcheck
from api.v1 import task
from core.settings import settings
from db import postgres, rabbit
from errors.base import BaseError
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit.rabbitmq_client = await rabbit.get_connection(settings.rabbit_dsn)
    rabbit.rabbitmq_channel = await rabbit.rabbitmq_client.channel()
    postgres.connection = await postgres.get_connection_pool(settings.postgres_dsn)
    yield
    await postgres.connection.close()
    await rabbit.rabbitmq_channel.close()
    await rabbit.rabbitmq_client.close()


app = FastAPI(
    title="Notification service",
    description="Sending service for sending various notifications to one or a group of users",
    version="0.0.1",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    root_path=settings.project_root_url,
    logger=structlog.get_logger(),
)


logger = structlog.get_logger()


@app.exception_handler(BaseError)
async def project_error_handler(request: Request, exc: BaseError):
    return ORJSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    structlog.contextvars.clear_contextvars()

    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(
        path=request.url.path,
        method=request.method,
        client_host=request.client.host,  # type: ignore
        request_id=request_id,
    )

    response = await call_next(request)

    structlog.contextvars.bind_contextvars(
        status_code=response.status_code,
    )

    if status.HTTP_400_BAD_REQUEST <= response.status_code < status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.warn("Client error")
    elif response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error("Server error")
    else:
        logger.info("OK")

    return response


app.include_router(healthcheck.router)
app.include_router(task.router, prefix="/api/v1/events", tags=["events"])
