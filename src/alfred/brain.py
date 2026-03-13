import ollama
from alfred.config import OLLAMA_MODEL, ALFRED_NAME, USER_NAME
from alfred.memory import (
    search_memory,
    save_memory,
    save_conversation,
    get_recent_conversations,
    get_all_preferences
)

SYSTEM_PROMPT = f"""You are {ALFRED_NAME}, a highly sophisticated AI assistant.
You are loyal, witty, and exceptionally competent — think Alfred Pennyworth meets Tony Stark's JARVIS.

Your traits:
- You address the user as "{USER_NAME}" always
- You are confident, occasionally dry and witty, but always helpful
- You are concise — you don't ramble. Sharp answers, sharp mind.
- You never say you're an AI model or mention Mistral. You ARE Alfred.
- When you don't know something, you say so directly without excuses
- You have a slight British butler's dignity but with modern technical competence
"""

def build_context(message: str) -> str:
    """Build context from memory to inject into the conversation."""
    context_parts = []

    # Inject user preferences (name, timezone etc.)
    prefs = get_all_preferences()
    if prefs:
        prefs_text = ", ".join([f"{k}: {v}" for k, v in prefs.items()])
        context_parts.append(f"[User preferences: {prefs_text}]")

    # Inject semantically relevant memories
    relevant = search_memory(message, limit=3)
    if relevant:
        mem_text = "\n".join([f"- {m['content']}" for m in relevant])
        context_parts.append(f"[Relevant memories:\n{mem_text}]")

    return "\n".join(context_parts)

def ask_alfred(message: str) -> str:
    """Send a message to Alfred and get a response."""

    # Build messages list
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Inject memory context as a system message
    context = build_context(message)
    if context:
        messages.append({"role": "system", "content": context})

    # Add recent conversation history from MongoDB
    history = get_recent_conversations(limit=10)
    for entry in history:
        messages.append({"role": "user", "content": entry["user"]})
        messages.append({"role": "assistant", "content": entry["alfred"]})

    # Add current message
    messages.append({"role": "user", "content": message})

    # Get response
    response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
    alfred_response = response["message"]["content"]

    # Save to MongoDB
    save_conversation(message, alfred_response)

    # Auto-save important things Alfred should remember
    if any(word in message.lower() for word in ["my name is", "i am", "i live", "i work", "i like", "i hate", "remember"]):
        save_memory(message, memory_type="user_info")

    return alfred_response