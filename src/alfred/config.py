from dotenv import load_dotenv
import os

load_dotenv()

# Ollama / LLM
OLLAMA_MODEL = "mistral-nemo"
OLLAMA_URL = "http://localhost:11434"

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
PIPER_EXE = os.getenv("PIPER_EXE", r"D:\piper\piper.exe")
PIPER_VOICE = os.getenv("PIPER_VOICE", r"D:\piper\voices\en_GB-northern_english_male-medium.onnx")

