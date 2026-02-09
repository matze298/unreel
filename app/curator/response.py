"""Module responsible for generating insights from text or topics using the Gemini API."""

from dataclasses import dataclass
from typing import Any

import orjson
import streamlit as st
from google import genai
from google.genai import types


@dataclass
class Insight:
    """Data class representing a single insight."""

    emoji: str = ""
    title: str = ""
    explanation: str = ""
    tag: str = ""
    expansion: str = ""


def generate_insights(
    api_key: str,
    source_text: str,
    *,
    is_topic_mode: bool,
    persona_instruction: str,
) -> list[Insight]:
    """The Brain: Sends text/topic to Gemini with instructions to expand/research.

    Args:
        api_key: Gemini API key.
        source_text: The input text or topic to analyze.
        is_topic_mode: If True, treat source_text as a topic; otherwise, as an article.
        persona_instruction: Additional instructions to shape the model's persona.

    Returns:
        A list of insights, where each insight is a dict with keys: emoji, title, explanation, expansion, tag.
    """
    client = genai.Client(api_key=api_key)

    # Dynamic preamble based on mode
    context_prompt: str = ""
    if is_topic_mode:
        context_prompt = (
            f"The user is interested in the topic: '{source_text}'. "
            "Search your internal knowledge base to find the most profound, "
            "high-value insights regarding this topic."
        )
    else:
        context_prompt = (
            "The user has provided an article (text below). Analyze it, BUT do not just summarize. "
            "Use your internal knowledge to EXPAND on the concepts found in the text. "
            "Add context that might be missing."
        )

    full_prompt: str = f"""
    You are an expert knowledge curator.

    TASK:
    {context_prompt}

    PERSONA INSTRUCTIONS:
    {persona_instruction}

    OUTPUT RULES:
    1. Identify 3 to 5 distinct, high-value insights.
    2. "Title": Catchy headline (max 8 words).
    3. "Explanation": Deep dive explanation (2-3 sentences).
    4. "Expansion": A specific sentence starting with "Did you know:" or "Pro Tip:" that adds value BEYOND the immediate topic/text.
    5. "Emoji": Relevant emoji.
    6. "Tag": Category tag (e.g., #Psychology).

    Format strictly as a JSON list of objects:
    [
        {{"emoji": "🧠", "title": "...", "explanation": "...", "expansion": "...", "tag": "..."}}
    ]

    INPUT CONTENT:
    {source_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=full_prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )

        # With JSON mode enabled, we can load the text directly
        if response.text is None:
            st.error("Gemini API Error: No text response received.")
            return []
        content: list[dict[str, Any]] = orjson.loads(response.text)
        return [Insight(**item) for item in content]

    except Exception as e:  # noqa: BLE001
        st.error(f"Gemini API Error: {e}")
        return []
