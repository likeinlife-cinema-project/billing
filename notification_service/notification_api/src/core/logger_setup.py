import logging
import logging.handlers
import sys
from pathlib import Path

import structlog


def configure_structlog(json_logging_level: str, console_logging_level: str, root_dir: Path):
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("aio_pika").setLevel(logging.ERROR)
    logging.getLogger("aiormq").setLevel(logging.ERROR)
    logging.basicConfig(format="%(message)s", stream=sys.stdout)
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

    log_dir = root_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    json_handler = logging.handlers.WatchedFileHandler(log_dir / "api.log")
    json_handler.setFormatter(formatter_json)
    json_handler.setLevel(json_logging_level)
    json_handler.set_name("JSON")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.NOTSET)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(json_handler)

    root_logger.handlers.pop(0)
