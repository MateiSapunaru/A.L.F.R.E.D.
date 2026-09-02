from dotenv import load_dotenv
import os

load_dotenv()

# Gemini / LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY must be set in your .env — see README setup.")

# MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "alfredDB"

# Collections
COLLECTION_MEMORIES = "alfredKnowledge"
COLLECTION_CONVERSATIONS = "conversations"
COLLECTION_TASKS = "tasks"
COLLECTION_PREFERENCES = "preferences"

# Alfred personality
ALFRED_NAME = "Alfred"
USER_NAME = "Sir"

# Voice
PIPER_EXE = os.getenv("PIPER_EXE")
PIPER_VOICE = os.getenv("PIPER_VOICE")

if not PIPER_EXE or not PIPER_VOICE:
    raise RuntimeError(
        "PIPER_EXE and PIPER_VOICE must be set in your .env — see README setup."
    )

