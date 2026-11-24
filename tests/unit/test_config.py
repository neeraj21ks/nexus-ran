import pytest

from nexus.core.config import clear_settings_cache, get_settings


@pytest.fixture(autouse=True)
def reset_settings(monkeypatch: pytest.MonkeyPatch):
    """Isolate configuration tests from the external environment."""
    for name in (
        "NEXUS_ENV",
        "NEXUS_LOG_LEVEL",
        "DATABASE_URL",
        "LLM_BASE_URL",
        "LLM_MODEL",
    ):
        monkeypatch.delenv(name, raising=False)

    clear_settings_cache()
    yield
    clear_settings_cache()


def test_default_settings() -> None:
    settings = get_settings()

    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.database_url is None
    assert settings.llm_base_url == "http://localhost:1234/v1"
    assert settings.llm_model is None


def test_environment_variable_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEXUS_ENV", "testing")
    monkeypatch.setenv("NEXUS_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/nexus")
    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:1234/v1/")
    monkeypatch.setenv("LLM_MODEL", "local-test-model")

    settings = get_settings()

    assert settings.environment == "testing"
    assert settings.log_level == "DEBUG"
    assert settings.database_url == "postgresql://localhost/nexus"
    assert settings.llm_base_url == "http://localhost:1234/v1"
    assert settings.llm_model == "local-test-model"


def test_environment_value_is_case_insensitive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NEXUS_ENV", "PRODUCTION")

    assert get_settings().environment == "production"


def test_invalid_environment_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NEXUS_ENV", "staging")

    with pytest.raises(ValueError, match="NEXUS_ENV"):
        get_settings()


def test_invalid_log_level_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NEXUS_LOG_LEVEL", "TRACE")

    with pytest.raises(ValueError, match="NEXUS_LOG_LEVEL"):
        get_settings()


def test_invalid_llm_url_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_BASE_URL", "localhost:1234/v1")

    with pytest.raises(ValueError, match="LLM_BASE_URL"):
        get_settings()


def test_empty_optional_values_become_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "  ")
    monkeypatch.setenv("LLM_MODEL", "  ")

    settings = get_settings()

    assert settings.database_url is None
    assert settings.llm_model is None
