from unittest.mock import MagicMock, patch

from alfred import memory


@patch("alfred.memory.memories")
def test_save_memory_stores_content_type_and_embedding(mock_memories):
    memory.save_memory("The user's name is John", memory_type="user_info")

    mock_memories.insert_one.assert_called_once()
    doc = mock_memories.insert_one.call_args[0][0]
    assert doc["content"] == "The user's name is John"
    assert doc["type"] == "user_info"
    assert "embedding" in doc
    assert "timestamp" in doc


@patch("alfred.memory.memories")
def test_search_memory_with_query_runs_vector_search(mock_memories):
    mock_memories.aggregate.return_value = [{"content": "likes tea", "type": "general"}]

    results = memory.search_memory("what does the user like", limit=3)

    assert results == [{"content": "likes tea", "type": "general"}]
    pipeline = mock_memories.aggregate.call_args[0][0]
    assert pipeline[0]["$vectorSearch"]["index"] == "vector_index"
    assert pipeline[0]["$vectorSearch"]["limit"] == 3


@patch("alfred.memory.memories")
def test_search_memory_without_query_returns_recent(mock_memories):
    cursor = MagicMock()
    cursor.sort.return_value.limit.return_value = [{"content": "recent memory"}]
    mock_memories.find.return_value = cursor

    results = memory.search_memory("", limit=5)

    assert results == [{"content": "recent memory"}]
    mock_memories.aggregate.assert_not_called()


@patch("alfred.memory.preferences")
def test_save_preference_upserts_by_key(mock_preferences):
    memory.save_preference("timezone", "Europe/Bucharest")

    mock_preferences.update_one.assert_called_once()
    filter_arg, update_arg = mock_preferences.update_one.call_args[0][:2]
    assert filter_arg == {"key": "timezone"}
    assert update_arg["$set"]["value"] == "Europe/Bucharest"
    assert mock_preferences.update_one.call_args[1]["upsert"] is True


@patch("alfred.memory.preferences")
def test_get_all_preferences_returns_dict(mock_preferences):
    mock_preferences.find.return_value = [
        {"key": "timezone", "value": "Europe/Bucharest"},
        {"key": "name", "value": "Sir"},
    ]

    result = memory.get_all_preferences()

    assert result == {"timezone": "Europe/Bucharest", "name": "Sir"}
