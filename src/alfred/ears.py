import threading
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import soundfile as sf

# Load Whisper model — base is fast and accurate enough for voice commands
model = whisper.load_model("base")

# Only one mic recording at a time — the hotkey listener and any UI "Talk"
# button both hit this, and overlapping sd.rec() calls on the same input
# device corrupt each other's audio.
_listen_lock = threading.Lock()

def listen(duration: int = 5, sample_rate: int = 16000) -> str:
    """Record from microphone and transcribe with Whisper."""
    with _listen_lock:
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

        # Boost quiet recordings up to a consistent peak level so Whisper
        # gets a strong signal even when mic gain/timing leaves it faint.
        # Skip near-total silence — normalizing that just amplifies noise.
        max_amp = float(np.abs(audio).max())
        if max_amp > 1e-4:
            audio = audio / max_amp * 0.95

        print("🧠 Transcribing...")
    
    # Save to temp file (Whisper needs a file, not raw audio)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, sample_rate)
        try:
            result = model.transcribe(f.name)
        except RuntimeError as e:
            # openai-whisper can throw "cannot reshape tensor of 0 elements"
            # on near-silent audio instead of just returning empty text.
            print(f"Transcription failed, likely silent/empty audio: {e}")
            return ""

    text = result["text"].strip()
    print(f"You said: {text}")
    return text