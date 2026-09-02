import keyboard
import requests
import threading

ALFRED_URL = "http://localhost:8000/listen"

def call_alfred():
    """Call the /listen endpoint in a separate thread."""
    print("\n🎤 Alfred is listening...")
    try:
        response = requests.post(ALFRED_URL, timeout=30)
        data = response.json()
        if "you" in data:
            print(f"You: {data['you']}")
            print(f"Alfred: {data['alfred']}")
    except Exception as e:
        print(f"Error: {e}")

def on_press():
    """Trigger Alfred in background thread so hotkey doesn't block."""
    thread = threading.Thread(target=call_alfred)
    thread.daemon = True
    thread.start()

print("🎩 Alfred hotkey active — press T to speak")
print("Press Ctrl+C to quit\n")

# Trigger on key press, not release, so there's no delay
keyboard.add_hotkey("T", on_press, trigger_on_release=False)

keyboard.wait("esc")  # Keep script running until ESC is pressed
