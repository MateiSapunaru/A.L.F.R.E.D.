# A.L.F.R.E.D.

A voice assistant I built to learn how modern AI stacks fit together. Think JARVIS but on a budget and without the Iron Man suit. Speech recognition, text-to-speech, and memory embeddings all run locally on my own hardware; the LLM call goes out to Google's Gemini API (free tier), which gave more consistent response times than local Ollama inference on this machine. It remembers things across conversations and talks back in a British accent.

Named after Alfred Pennyworth, obviously.

---

## What it does

- You press a hotkey, talk, and it responds out loud
- It remembers what you've told it across sessions — not just the last conversation
- When you say something like "my name is John" or "I work in tech", it stores that and recalls it when relevant
- Speech recognition, text-to-speech, and embeddings run locally — only the chat message and memory context are sent to Gemini's API for the LLM call

---

## Stack

| | |
|---|---|
| LLM | Gemini 3.6 Flash (Google AI API, free tier) |
| Speech recognition | OpenAI Whisper (local) |
| Text to speech | Piper TTS |
| Backend | FastAPI |
| Database | MongoDB Atlas |
| Memory search | MongoDB Atlas Vector Search |
| Embeddings | all-MiniLM-L6-v2 |
| Package management | Poetry |

I went with MongoDB for everything — conversations, preferences, and vector memory — rather than running a separate vector database alongside it. Atlas Vector Search handles semantic similarity well enough for this use case and it keeps the stack simpler.

---

## Project structure

```
alfred/
├── src/alfred/
│   ├── main.py        # FastAPI app and endpoints
│   ├── brain.py       # Gemini interface, personality prompt, memory injection
│   ├── memory.py      # Save/search memories, conversation history, preferences
│   ├── database.py    # MongoDB connection
│   ├── ears.py        # Whisper recording and transcription
│   ├── voice.py       # Piper TTS playback
│   └── config.py      # Settings and env vars
├── hotkey.py          # Global push-to-talk listener
├── streamlit_app.py   # Text/voice chat UI
├── .env
└── pyproject.toml
```

---

## Setup

You'll need:
- Python 3.11+
- A free [Gemini API key](https://aistudio.google.com/apikey) from Google AI Studio
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) on your PATH
- [Piper TTS](https://github.com/rhasspy/piper/releases) — grab the Windows binary and a voice model from the [samples page](https://rhasspy.github.io/piper-samples/)
- A free [MongoDB Atlas](https://mongodb.com/atlas) cluster — remember to add your IP to Atlas's Network Access list, or the app can't reach the database

**Install dependencies:**
```bash
poetry install
```

**Create your `.env`:**
```env
MONGODB_URI=<example>
PIPER_EXE=<example>
PIPER_VOICE=<example>
GEMINI_API_KEY=<example>
```

**Set up the vector search index in Atlas:**

On your `alfredKnowledge` collection, create an Atlas Vector Search index named `vector_index`:
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 384,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "type"
    }
  ]
}
```

---

## Running it

Start the server:
```bash
poetry run uvicorn alfred.main:app --reload
```

Start the hotkey listener in a second terminal:
```bash
poetry run python hotkey.py
```

Press **T** to talk. Alfred listens for 5 seconds then responds.

The API is at `http://localhost:8000` — Swagger docs at `/docs` if you want to poke around.

There's also a small Streamlit UI for chatting with Alfred over text (and triggering voice mode) without needing the hotkey:
```bash
poetry run streamlit run streamlit_app.py
```

---

## API

| Method | Endpoint | |
|---|---|---|
| GET | `/` | health check |
| POST | `/chat` | text in, text out |
| POST | `/listen` | mic in, voice out |
| POST | `/memory` | manually save something |
| GET | `/memories` | see what it remembers |
| POST | `/preference` | save a preference |
| GET | `/preferences` | get all preferences |

---

## What's next

- [ ] Calculator (natural language math)
- [ ] Calendar and reminders
- [ ] Task lists
- [ ] Web search

---

## Hardware

Built and tested on Windows 11 with an RTX 4070 12GB. Whisper uses the `base` model which is fast enough for real-time use on CPU or GPU.
