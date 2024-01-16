import os

import structlog

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "json_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=True),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": (
                "plain_console" if os.getenv("DJANGO_ADMIN_BILLING_DEBUG", "False") == "True" else "json_console"
            ),
            "level": os.getenv("LOGGING_LEVEL", "DEBUG"),
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": os.getenv("LOGGING_LEVEL", "DEBUG"),
        },
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
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
