"""Module responsible for fetching and parsing content from URLs, specifically news articles."""

import requests
from bs4 import BeautifulSoup


def fetch_article_content(url: str) -> tuple[str | None, str]:
    """Fetches the title and text content of a news article from the given URL.

    Args:
        url: The URL of the news article to fetch.

    Returns:
        A tuple containing the title of the article (or None if not found) and the text content.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = soup.title.string if soup.title else "No Title Found"

        # Extract paragraphs (basic scraping)
        paragraphs = soup.find_all("p")
        text_content = "\n".join([p.get_text() for p in paragraphs])

        # Limit text to avoid token limits (Gemini has a large window, but let's be safe)
        return title, text_content[:25000]
    except Exception as e:  # noqa: BLE001
        return None, f"Error fetching URL: {e}"
