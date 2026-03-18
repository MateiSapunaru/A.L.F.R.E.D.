# A.L.F.R.E.D.

A locally-running AI assistant I built to learn how modern AI stacks fit together. Think JARVIS but on a budget and without the Iron Man suit. It runs entirely on my own hardware, remembers things across conversations, and talks back in a British accent.

Named after Alfred Pennyworth, obviously.

---

## What it does

- You press a hotkey, talk, and it responds out loud
- It remembers what you've told it across sessions — not just the last conversation
- When you say something like "my name is John" or "I work in tech", it stores that and recalls it when relevant
- Runs 100% locally. No API calls to OpenAI, no subscription fees, nothing leaves your machine except MongoDB data

---

## Stack

| | |
|---|---|
| LLM | Mistral Nemo via Ollama |
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
│   ├── brain.py       # Ollama interface, personality prompt, memory injection
│   ├── memory.py      # Save/search memories, conversation history, preferences
│   ├── database.py    # MongoDB connection
│   ├── ears.py        # Whisper recording and transcription
│   ├── voice.py       # Piper TTS playback
│   └── config.py      # Settings and env vars
├── hotkey.py          # Global push-to-talk listener
├── .env
└── pyproject.toml
```

---

## Setup

You'll need:
- Python 3.11+
- [Ollama](https://ollama.com) — `ollama pull mistral-nemo`
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) on your PATH
- [Piper TTS](https://github.com/rhasspy/piper/releases) — grab the Windows binary and a voice model from the [samples page](https://rhasspy.github.io/piper-samples/)
- A free [MongoDB Atlas](https://mongodb.com/atlas) cluster

**Install dependencies:**
```bash
poetry install
```

**Create your `.env`:**
```env
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/alfredDB
PIPER_EXE=D:\piper\piper.exe
PIPER_VOICE=D:\piper\voices\en_GB-northern_english_male-medium.onnx
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

Hold **numpad Enter** to talk. Alfred listens for 5 seconds then responds.

The API is at `http://localhost:8000` — Swagger docs at `/docs` if you want to poke around.

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

Built and tested on Windows 11 with an RTX 4070 12GB. Mistral Nemo runs comfortably on the GPU via Ollama. Whisper uses the `base` model which is fast enough for real-time use.
