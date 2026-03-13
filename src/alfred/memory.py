from datetime import datetime
from sentence_transformers import SentenceTransformer
from alfred.database import memories, conversations, preferences

# Load the embedding model — small, fast, runs on your GPU
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    """Convert text to vector embedding."""
    return embedder.encode(text).tolist()

# ── Semantic Memory ────────────────────────────────────────────────

def save_memory(content: str, memory_type: str = "general"):
    """Save something to Alfred's long-term memory with embedding."""
    memories.insert_one({
        "content": content,
        "type": memory_type,
        "embedding": get_embedding(content),
        "timestamp": datetime.utcnow()
    })

def search_memory(query: str, limit: int = 5) -> list:
    """Find relevant memories using vector search."""
    if not query:
        # Just return recent memories if no query
        results = memories.find(
            {},
            {"content": 1, "type": 1, "timestamp": 1, "_id": 0}
        ).sort("timestamp", -1).limit(limit)
        return list(results)
    
    query_embedding = get_embedding(query)
    
    results = memories.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 50,
                "limit": limit
            }
        },
        {
            "$project": {
                "content": 1,
                "type": 1,
                "timestamp": 1,
                "score": {"$meta": "vectorSearchScore"},
                "_id": 0
            }
        }
    ])
    
    return list(results)

# ── Conversation History ───────────────────────────────────────────

def save_conversation(user_message: str, alfred_response: str):
    """Persist conversation to MongoDB."""
    conversations.insert_one({
        "user": user_message,
        "alfred": alfred_response,
        "timestamp": datetime.utcnow()
    })

def get_recent_conversations(limit: int = 10) -> list:
    """Get last N conversations for context."""
    results = conversations.find(
        {},
        {"user": 1, "alfred": 1, "_id": 0}
    ).sort("timestamp", -1).limit(limit)
    
    # Reverse so oldest is first (natural conversation order)
    return list(reversed(list(results)))

# ── User Preferences ──────────────────────────────────────────────

def save_preference(key: str, value: str):
    """Save or update a user preference."""
    preferences.update_one(
        {"key": key},
        {"$set": {"key": key, "value": value, "updated": datetime.utcnow()}},
        upsert=True
    )

def get_preference(key: str) -> str | None:
    """Get a user preference by key."""
    result = preferences.find_one({"key": key})
    return result["value"] if result else None

def get_all_preferences() -> dict:
    """Get all user preferences as a dictionary."""
    results = preferences.find({}, {"key": 1, "value": 1, "_id": 0})
    return {r["key"]: r["value"] for r in results}

