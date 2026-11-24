import json
import logging

from nexus.core.config import get_settings
from nexus.core.logging import JsonFormatter, configure_logging


def test_json_formatter_outputs_valid_json() -> None:
    record = logging.LogRecord(
        name="nexus.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    output = JsonFormatter().format(record)
    payload = json.loads(output)

    assert payload["level"] == "INFO"
    assert payload["logger"] == "nexus.test"
    assert payload["message"] == "Test message"
    assert payload["timestamp"].endswith("+00:00")


def test_json_formatter_includes_exception_details() -> None:
    try:
        raise ValueError("Simulated test exception")
    except ValueError:
        record = logging.LogRecord(
            name="nexus.test",
            level=logging.ERROR,
            pathname=__file__,
            lineno=20,
            msg="Operation failed",
            args=(),
            exc_info=__import__("sys").exc_info(),
        )

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "ERROR"
    assert "ValueError: Simulated test exception" in payload["exception"]


def test_configure_logging_returns_nexus_logger() -> None:
    logger = configure_logging()

    assert logger.name == "nexus"
    assert logger.level == logging.INFO
    assert logger.propagate is False


def test_configure_logging_uses_configured_log_level() -> None:
    settings = get_settings()
    logger = configure_logging(settings)

    assert logger.level == logging.INFO
    assert len(logger.handlers) >= 1
    assert isinstance(logger.handlers[0].formatter, JsonFormatter)
