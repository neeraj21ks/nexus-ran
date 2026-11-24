"""Structured JSON logging for NEXUS RAN."""

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any

from nexus.core.config import Settings, get_settings


class JsonFormatter(logging.Formatter):
    """Format log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Convert a log record into a JSON string."""
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)

        return json.dumps(payload, default=str)


def configure_logging(settings: Settings | None = None) -> logging.Logger:
    """Configure and return the NEXUS application logger."""
    configuration = settings or get_settings()

    logger = logging.getLogger("nexus")
    logger.setLevel(configuration.log_level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    for handler in logger.handlers:
        handler.setLevel(configuration.log_level)

    return logger
