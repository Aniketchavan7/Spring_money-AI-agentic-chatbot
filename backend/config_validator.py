"""Spring Money configuration validator and environment checker."""

import os
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AgentRuntimeConfig(BaseModel):
    retriever: str = Field(default="tavily", description="Default search retriever")
    llm_provider: str = Field(default="ollama", description="LLM provider name")
    fast_llm_model: str = Field(default="llama3:8b", description="Fast model identifier")
    smart_llm_model: str = Field(default="llama3:70b", description="Reasoning model identifier")
    llm_base_url: Optional[str] = Field(default=None, description="Local or private model endpoint")
    temperature: float = Field(default=0.55, ge=0.0, le=2.0)
    max_search_results: int = Field(default=5, ge=1, le=50)
    report_format: str = Field(default="APA")


def validate_runtime_environment() -> Dict[str, any]:
    """Inspect environment variables and return validated configuration and warnings."""
    warnings: List[str] = []
    
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
        warnings.append("OPENAI_API_KEY is not set while LLM_PROVIDER is configured to 'openai'")
    elif provider == "google" and not os.getenv("GEMINI_API_KEY"):
        warnings.append("GEMINI_API_KEY is not set while LLM_PROVIDER is configured to 'google'")
    elif provider == "ollama" and not os.getenv("LLM_BASE_URL"):
        # Default fallback to standard local Ollama port
        os.environ["LLM_BASE_URL"] = "http://localhost:11434"

    retriever = os.getenv("RETRIEVER", "tavily").lower()
    if retriever == "tavily" and not os.getenv("TAVILY_API_KEY"):
        warnings.append("TAVILY_API_KEY is unset; live search queries will require mock fallback")

    config = AgentRuntimeConfig(
        retriever=retriever,
        llm_provider=provider,
        fast_llm_model=os.getenv("FAST_LLM_MODEL", "llama3:8b"),
        smart_llm_model=os.getenv("SMART_LLM_MODEL", "llama3:70b"),
        llm_base_url=os.getenv("LLM_BASE_URL"),
        temperature=float(os.getenv("TEMPERATURE", 0.55)),
        max_search_results=int(os.getenv("MAX_SEARCH_RESULTS_PER_QUERY", 5)),
        report_format=os.getenv("REPORT_FORMAT", "APA"),
    )

    return {
        "valid": len(warnings) == 0,
        "warnings": warnings,
        "config": config.model_dump(),
    }
