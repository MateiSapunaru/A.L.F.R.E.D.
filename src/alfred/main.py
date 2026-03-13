from fastapi import FastAPI
from pydantic import BaseModel
from alfred.brain import ask_alfred
from alfred.database import ping
from alfred.memory import save_preference, get_all_preferences, save_memory, search_memory
from alfred.ears import listen
from alfred.voice import speak

app = FastAPI(title="Alfred", description="Your personal AI assistant")

class Message(BaseModel):
    text: str

class Preference(BaseModel):
    key: str
    value: str

@app.on_event("startup")
def startup():
    if ping():
        print("Alfred is online. MongoDB connected.")
    else:
        print("Warning: MongoDB connection failed.")

@app.get("/")
def root():
    return {"status": "Alfred is online, Sir."}

@app.post("/chat")
def chat(message: Message):
    response = ask_alfred(message.text)
    return {"response": response}

@app.post("/memory")
def add_memory(message: Message):
    save_memory(message.text, memory_type="manual")
    return {"status": "Committed to memory, Sir."}

@app.post("/preference")
def set_preference(pref: Preference):
    save_preference(pref.key, pref.value)
    return {"status": f"Noted, Sir. {pref.key} set to {pref.value}."}

@app.get("/preferences")
def get_preferences():
    return get_all_preferences()

@app.get("/memories")
def get_memories():
    results = search_memory("", limit=20)
    return {"memories": results}

@app.post("/listen")
def listen_and_respond():
    """Listen from mic, talk to Alfred, speak the response."""
    # Listen
    user_input = listen(duration=5)
    
    if not user_input:
        speak("I didn't catch that, Sir. Could you repeat yourself?")
        return {"status": "no input detected"}
    
    # Think
    response = ask_alfred(user_input)
    
    # Speak
    speak(response)
    
    return {
        "you": user_input,
        "alfred": response
    }