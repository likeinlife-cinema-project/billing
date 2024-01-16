import uuid
from contextlib import asynccontextmanager

import structlog
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from auth_app.api import healthcheck
from auth_app.api.v1 import auth, oauth, role, user, user_role
from auth_app.core.config import settings as s
from auth_app.core.jaeger import configure_tracer, jaeger_middleware
from auth_app.db import redis, sqlalchemy
from auth_app.errors.base import BaseErrorWithDetail


def create_engine_() -> AsyncEngine:
    if s.debug:
        engine = create_async_engine(
            s.database_dsn.unicode_string(),
            echo=True,
            future=True,
        )
    else:
        engine = create_async_engine(
            s.database_dsn.unicode_string(),
            future=True,
        )

    return engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=s.redis.host, port=s.redis.port)
    await FastAPILimiter.init(redis.redis)
    sqlalchemy.engine = create_engine_()
    yield
    await redis.redis.close()
    sqlalchemy.engine = None


logger = structlog.get_logger()

app = FastAPI(
    title="Auth сервис",
    description="Сервис авторизации, аутентификации",
    version="0.0.1",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    dependencies=[Depends(RateLimiter(times=s.request_limit_per_minute, minutes=1))],
    root_path=s.project_root_url,
    logger=structlog.get_logger(),
)


@app.middleware("http")
async def schema_correct(request: Request, call_next):
    scheme = "https" if request.headers.get("X-Forwarded-Proto") == "https" else "http"
    request.scope["scheme"] = scheme

    response = await call_next(request)

    return response


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    structlog.contextvars.clear_contextvars()

    structlog.contextvars.bind_contextvars(
        path=request.url.path,
        method=request.method,
        client_host=request.client.host,  # type: ignore
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


if not s.debug:
    configure_tracer(service_name=s.project_name, host=s.jaeger.host, port=s.jaeger.port)
    app.middleware("http")(jaeger_middleware)
    FastAPIInstrumentor.instrument_app(app)


@app.exception_handler(BaseErrorWithDetail)
async def app_exception_handler(request: Request, exc: BaseErrorWithDetail):
    return ORJSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


app.add_middleware(
    CorrelationIdMiddleware,
    generator=lambda: str(uuid.uuid4()),
    header_name="x-request-id",
)


app.include_router(healthcheck.router)
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(user.router, prefix="/api/v1/user")
app.include_router(role.router, prefix="/api/v1/role")
app.include_router(user_role.router, prefix="/api/v1/role")
app.include_router(oauth.router, prefix="/api/v1/oauth")
