import os
from backend.config_validator import validate_runtime_environment, AgentRuntimeConfig


def test_default_config_generation():
    """Ensure default configuration creates valid instance."""
    result = validate_runtime_environment()
    assert "config" in result
    assert result["config"]["retriever"] in ["tavily", "google", "bing"]
    assert result["config"]["temperature"] >= 0.0


def test_agent_runtime_config_bounds():
    """Verify pydantic bounds for configuration."""
    cfg = AgentRuntimeConfig(temperature=0.8, max_search_results=10)
    assert cfg.temperature == 0.8
    assert cfg.max_search_results == 10
