"""Text processing functions"""
import urllib
from typing import Dict, Generator, Optional

from selenium.webdriver.remote.webdriver import WebDriver

try:
    from gpt_researcher.config.config import Config
except ImportError:
    Config = None

try:
    from gpt_researcher.utils.llm import create_chat_completion
except ImportError:
    create_chat_completion = None

import os


def split_text(text: str, max_length: int = 8192) -> Generator[str, None, None]:
    """Split text into chunks of a maximum length

    Args:
        text (str): The text to split
        max_length (int, optional): The maximum length of each chunk. Defaults to 8192.

    Yields:
        str: The next chunk of text

    Raises:
        ValueError: If the text is longer than the maximum length
    """
    paragraphs = text.split("\n")
    current_length = 0
    current_chunk = []

    for paragraph in paragraphs:
        if current_length + len(paragraph) + 1 <= max_length:
            current_chunk.append(paragraph)
            current_length += len(paragraph) + 1
        else:
            yield "\n".join(current_chunk)
            current_chunk = [paragraph]
            current_length = len(paragraph) + 1

    if current_chunk:
        yield "\n".join(current_chunk)


def summarize_text(
    fast_llm_model: str, summary_token_limit: int, llm_provider: str, url: str, text: str, question: str, driver: Optional[WebDriver] = None
) -> str:
    """Summarize text using the LLM API

    Args:
        fast_llm_model (str): The fast LLM model e.g gpt3.5-turbo-16k
        summary_token_limit (int): The summary token limit
        llm_provider (str): The LLM provider (e.g. openai, ollama)
        url (str): The URL of the text
        text (str): The text to summarize
        question (str): The question to answer
        driver (WebDriver): The webdriver instance

    Returns:
        str: The summary of the text
    """
    if not text:
        return "No text to summarize"

    summary = ""
    paragraphs = split_text(text, 8192)

    for paragraph in paragraphs:
        if create_chat_completion:
            summary = create_chat_completion(
                model=fast_llm_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Summarize the following text for the question: '{question}':\n\n{paragraph}"},
                ],
                temperature=0.5,
                max_tokens=summary_token_limit,
                provider=llm_provider,
            )
        else:
            summary = paragraph[:summary_token_limit]

    return summary
