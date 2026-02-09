"""Tests the response module of the curator package."""

from unittest.mock import MagicMock, patch

import pytest

from app.curator.response import Insight, generate_insights


@pytest.mark.parametrize(
    ("api_key", "source_text", "is_topic_mode", "persona_instruction"),
    [
        ("fake_api_key", "Artificial Intelligence", True, "Be concise and insightful."),
        (
            "fake_api_key",
            "The impact of climate change on polar bears.",
            False,
            "Focus on ecological and biological insights.",
        ),
    ],
)
def test_generate_insights(api_key: str, source_text: str, *, is_topic_mode: bool, persona_instruction: str) -> None:
    """Tests the generate_insights function with various inputs."""
    # GIVEN an API key, source text, mode, and persona instruction

    # GIVEN a mocked client.models.generate_content
    with patch("app.curator.response.genai.Client") as mock_client:
        mock_client.return_value.models.generate_content = MagicMock(
            return_value=MagicMock(
                text='[{"emoji": "💡", "title": "Insight 1", "explanation": "Explanation 1", "expansion":'
                '"Expansion 1", "tag": "#Tag1}]',
            ),
        )

        # WHEN generate_insights is called
        insights = generate_insights(
            api_key, source_text, is_topic_mode=is_topic_mode, persona_instruction=persona_instruction
        )

        # THEN it should return a list of insights
        assert isinstance(insights, list)

        # THEN the content should be parsed correctly into Insight objects
        for insight in insights:
            assert isinstance(insight, Insight)
            assert insight.emoji == "💡"
            assert insight.title == "Insight 1"
            assert insight.explanation == "Explanation 1"
            assert insight.expansion == "Expansion 1"
            assert insight.tag == "#Tag1"
