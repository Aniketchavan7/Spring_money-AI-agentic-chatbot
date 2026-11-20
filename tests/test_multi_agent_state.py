import json
import os
import pytest
from multi_agents.memory.draft import DraftState
from multi_agents.memory.research import ResearchState


def test_task_json_parsing():
    """Verify task.json config conforms to schema."""
    task_path = os.path.join(os.path.dirname(__file__), "..", "multi_agents", "task.json")
    assert os.path.exists(task_path)

    with open(task_path, "r", encoding="utf-8") as f:
        task = json.load(f)

    assert "query" in task
    assert isinstance(task["query"], str)
    assert "publish_formats" in task
    assert "markdown" in task["publish_formats"]
    assert isinstance(task.get("max_sections", 3), int)


def test_draft_state_instantiation():
    """Ensure DraftState schema holds valid keys."""
    state: DraftState = {
        "task": {"query": "Test Financial Query"},
        "topic": "Market Trends",
        "draft": {"title": "Test Title", "content": "Body text"},
        "review": "Approved",
        "revision_notes": "None",
    }
    assert state["topic"] == "Market Trends"
    assert state["review"] == "Approved"


def test_research_state_structure():
    """Ensure ResearchState accommodates full report schema."""
    state: ResearchState = {
        "task": {"query": "Q3 Earnings"},
        "initial_research": "Initial insights",
        "sections": ["Overview", "Analysis", "Outlook"],
        "research_data": [{"source": "SEC Filings", "data": "10-Q"}],
        "title": "Q3 Financial Report",
        "headers": {"sec1": "Overview"},
        "date": "2026-11-20",
        "table_of_contents": "1. Overview",
        "introduction": "This report examines Q3 results.",
        "conclusion": "Positive trajectory.",
        "sources": ["https://sec.gov"],
        "report": "# Full Report Text",
    }
    assert len(state["sections"]) == 3
    assert len(state["sources"]) == 1
    assert state["report"].startswith("# Full Report")
