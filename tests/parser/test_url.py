"""Unit tests for the URL parsing functionality in the parser module."""

from unittest.mock import MagicMock, patch

import pytest

from app.parser.url import fetch_article_content


@pytest.mark.parametrize(
    ("url", "expected_title", "expected_content_start"),
    [
        ("http://example.com/article1", "Example Article 1", "This is the content of article 1."),
        ("http://example.com/article2", "Example Article 2", "This is the content of article 2."),
    ],
)
def test_fetch_article_content(url: str, expected_title: str, expected_content_start: str) -> None:
    """Tests the fetch_article_content function with various URLs."""
    # GIVEN a URL, an expected title, and expected content start

    # GIVEN a mocked requests.get that returns a successful response with HTML content
    with patch("app.parser.url.requests.get") as mock_get:
        # Mock a successful response with HTML content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            f"<html><head><title>{expected_title}</title></head><body><p>{expected_content_start}...</p></body></html>"
        )
        mock_get.return_value = mock_response

        # WHEN fetch_article_content is called
        title, content = fetch_article_content(url)

        # THEN the title and content should match expectations
        assert title == expected_title
        assert content.startswith(expected_content_start)


def test_fetch_article_content_invalid_url() -> None:
    """Tests the fetch_article_content function with an invalid URL."""
    # GIVEN an invalid URL
    # GIVEN a mocked requests.get that raises an exception
    with patch("app.parser.url.requests.get") as mock_get:
        # Mock a failed response (e.g., invalid URL)
        mock_get.side_effect = Exception("Invalid URL")

    # WHEN fetch_article_content is called
    title, content = fetch_article_content("http://invalid-url")

    # THEN it should return None for title and an error message for content
    assert title is None
    assert content.startswith("Error fetching URL:")
