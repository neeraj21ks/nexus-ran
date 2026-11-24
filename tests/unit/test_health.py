from datetime import UTC, datetime

from nexus.core.health import get_health_status


def test_health_status_returns_healthy_state() -> None:
    health = get_health_status()

    assert health.status == "healthy"
    assert health.service == "nexus-ran"
    assert health.version == "0.1.0"


def test_health_status_contains_valid_utc_timestamp() -> None:
    health = get_health_status()

    timestamp = datetime.fromisoformat(health.timestamp)

    assert timestamp.tzinfo is not None
    assert timestamp.utcoffset() == UTC.utcoffset(timestamp)


def test_health_status_can_be_serialized() -> None:
    health = get_health_status()

    result = health.to_dict()

    assert isinstance(result, dict)
    assert result["status"] == "healthy"
    assert result["service"] == "nexus-ran"
