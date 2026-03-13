import whisper
import sounddevice as sd
import numpy as np
import tempfile
import soundfile as sf

# Load Whisper model — base is fast and accurate enough for voice commands
model = whisper.load_model("base")

def listen(duration: int = 5, sample_rate: int = 16000) -> str:
    """Record from microphone and transcribe with Whisper."""
    print("🎤 Listening...")
    
    # Record audio
    audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32",
    device=None  # Use default input device
    )
    sd.wait()  # Wait until recording is done
    
    print("🧠 Transcribing...")
    
    # Save to temp file (Whisper needs a file, not raw audio)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, sample_rate)
        result = model.transcribe(f.name)
    
    text = result["text"].strip()
    print(f"You said: {text}")
    return text