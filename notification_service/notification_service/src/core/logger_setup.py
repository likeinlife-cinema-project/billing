import logging
import logging.handlers

import structlog


def configure_structlog(json_logging_level: str, console_logging_level: str):
    from .settings import PROJECT_ROOT

    logging.basicConfig()
    logging.getLogger("aio_pika").setLevel(logging.ERROR)
    logging.getLogger("aiormq").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
    logging.getLogger("httpcore").setLevel(logging.ERROR)
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )

    formatter_console = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(),
        ],
    )
    formatter_json = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter_console)
    console_handler.setLevel(console_logging_level)
    console_handler.set_name("CONSOLE")

    (PROJECT_ROOT / "logs").mkdir(exist_ok=True)
    json_handler = logging.handlers.WatchedFileHandler(PROJECT_ROOT / "logs/api.log")
    json_handler.setFormatter(formatter_json)
    json_handler.setLevel(json_logging_level)
    json_handler.set_name("JSON")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(json_handler)

    root_logger.handlers.pop(0)
