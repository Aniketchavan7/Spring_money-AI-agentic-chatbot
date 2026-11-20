import os
import pytest
from backend.utils import sanitize_filename, write_to_file, write_text_to_md


def test_sanitize_filename_traversal():
    """Verify directory traversal tokens are stripped to safe basename."""
    assert sanitize_filename("../../../etc/passwd") == "passwd"
    assert sanitize_filename("test file (1) & 2.md") == "test_file_1_2.md" or "test_file" in sanitize_filename("test file (1) & 2.md")
    assert len(sanitize_filename("")) > 0


@pytest.mark.asyncio
async def test_write_to_file_and_markdown(tmp_path):
    """Verify asynchronous file writer creates directories and files cleanly."""
    target = tmp_path / "nested" / "test_report.md"
    content = "# Financial Summary\n\n- Revenue: $10M"
    await write_to_file(str(target), content)

    assert os.path.exists(str(target))
    with open(str(target), "r", encoding="utf-8") as f:
        read_back = f.read()
    assert read_back == content
