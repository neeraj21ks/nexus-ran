"""Centralized NEXUS RAN application configuration."""

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

Environment = Literal["development", "testing", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated application configuration."""

    environment: Environment
    log_level: LogLevel
    database_url: str | None
    llm_base_url: str
    llm_model: str | None


def _required_choice(
    name: str,
    value: str,
    allowed: tuple[str, ...],
) -> str:
    """Validate an environment variable against allowed values."""
    normalized = value.strip().lower() if name == "NEXUS_ENV" else value.strip().upper()

    if normalized not in allowed:
        choices = ", ".join(allowed)
        raise ValueError(f"{name} must be one of: {choices}")

    return normalized


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and validate settings from environment variables."""
    environment = _required_choice(
        "NEXUS_ENV",
        os.getenv("NEXUS_ENV", "development"),
        ("development", "testing", "production"),
    )

    log_level = _required_choice(
        "NEXUS_LOG_LEVEL",
        os.getenv("NEXUS_LOG_LEVEL", "INFO"),
        ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    )

    llm_base_url = os.getenv(
        "LLM_BASE_URL",
        "http://localhost:1234/v1",
    ).strip().rstrip("/")

    if not llm_base_url.startswith(("http://", "https://")):
        raise ValueError("LLM_BASE_URL must start with http:// or https://")

    database_url = os.getenv("DATABASE_URL", "").strip() or None
    llm_model = os.getenv("LLM_MODEL", "").strip() or None

    return Settings(
        environment=environment,  # type: ignore[arg-type]
        log_level=log_level,  # type: ignore[arg-type]
        database_url=database_url,
        llm_base_url=llm_base_url,
        llm_model=llm_model,
    )


def clear_settings_cache() -> None:
    """Clear cached settings, primarily for tests."""
    get_settings.cache_clear()
