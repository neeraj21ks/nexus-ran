"""Core health-check models and service."""

from dataclasses import asdict, dataclass
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class HealthStatus:
    """Represents the health of the NEXUS RAN application."""

    status: str
    service: str
    version: str
    timestamp: str

    def to_dict(self) -> dict[str, str]:
        """Return the health status as a JSON-compatible dictionary."""
        return asdict(self)


def get_health_status() -> HealthStatus:
    """Return the current application health status."""
    from nexus import __version__

    return HealthStatus(
        status="healthy",
        service="nexus-ran",
        version=__version__,
        timestamp=datetime.now(UTC).isoformat(),
    )
