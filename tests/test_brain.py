from unittest.mock import patch

from alfred.brain import build_context


@patch("alfred.brain.search_memory")
@patch("alfred.brain.get_all_preferences")
def test_build_context_includes_preferences_and_memories(mock_prefs, mock_search):
    mock_prefs.return_value = {"name": "Sir", "timezone": "Europe/Bucharest"}
    mock_search.return_value = [{"content": "likes tea"}, {"content": "works in tech"}]

    context = build_context("what do you know about me")

    assert "name: Sir" in context
    assert "timezone: Europe/Bucharest" in context
    assert "- likes tea" in context
    assert "- works in tech" in context


@patch("alfred.brain.search_memory")
@patch("alfred.brain.get_all_preferences")
def test_build_context_empty_when_nothing_relevant(mock_prefs, mock_search):
    mock_prefs.return_value = {}
    mock_search.return_value = []

    assert build_context("hello") == ""
