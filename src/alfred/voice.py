import subprocess
import tempfile
import sounddevice as sd
import soundfile as sf
from alfred.config import PIPER_EXE, PIPER_VOICE

def speak(text: str):
    """Convert text to speech using Piper and play it."""
    print(f"Alfred: {text}")
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        output_file = f.name
    
    # Run Piper to generate audio
    subprocess.run(
        [PIPER_EXE, "--model", PIPER_VOICE, "--output_file", output_file],
        input=text.encode(),
        capture_output=True
    )
    
    # Play the generated audio
    audio, sample_rate = sf.read(output_file)
    sd.play(audio, sample_rate)
    device = None  # Use default output device
    sd.wait()