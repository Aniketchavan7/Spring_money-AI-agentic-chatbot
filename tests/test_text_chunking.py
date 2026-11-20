"""Unit tests for text processing and paragraph chunking generators."""

import pytest
from scraping.processing.text import split_text


def test_split_text_small_input():
    """Verify text shorter than max_length yields single chunk."""
    text = "Line 1: Q3 financial report\nLine 2: Revenue surged 15%\nLine 3: Operating margin expanded"
    chunks = list(split_text(text, max_length=500))
    assert len(chunks) == 1
    assert chunks[0] == text


def test_split_text_chunk_boundaries():
    """Verify generator yields multiple chunks when text exceeds max_length."""
    paragraphs = [f"Paragraph {i}: " + ("x" * 60) for i in range(10)]
    full_text = "\n".join(paragraphs)

    # Chunk with max_length of 150
    chunks = list(split_text(full_text, max_length=150))
    assert len(chunks) > 1

    # Ensure every chunk is within limit
    for chunk in chunks:
        assert len(chunk) <= 150

    # Ensure all content is retained
    reconstructed = "\n".join(chunks)
    assert reconstructed == full_text
