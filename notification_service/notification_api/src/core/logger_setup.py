import logging

import structlog
from structlog.types import EventDict


def healthcheck_filter(_, __, event_dict: EventDict) -> EventDict:
    if event_dict.get("path", "").endswith("/health/"):
        raise structlog.DropEvent
    return event_dict


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        healthcheck_filter,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.MODULE,
            ],
        ),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=structlog.threadlocal.wrap_dict(dict),
    cache_logger_on_first_use=True,
)

FOREIGN_PRE_CHAIN = (
    [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.MODULE,
            ],
        ),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ],
)


def get_logging_settings(logging_level: str, debug_mode: bool):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json_console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
                "keep_exc_info": True,
                "foreign_pre_chain": FOREIGN_PRE_CHAIN,
            },
            "plain_console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=True),
                "keep_exc_info": True,
                "foreign_pre_chain": FOREIGN_PRE_CHAIN,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": ("plain_console" if debug_mode else "json_console"),
                "level": logging_level,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": logging_level,
            },
            "uvicorn.access": {"level": logging.ERROR},
            "uvicorn.error": {"level": logging.ERROR},
            "aio_pika": {"level": logging.ERROR},
            "aiormq": {"level": logging.ERROR},
        },
    }
