from gtts import gTTS
import os

def speak(text, lang='en'):
    tts = gTTS(text, lang=lang)
    out = os.path.expanduser("~/voice.mp3")
    tts.save(out)
    os.system(f"mpv --really-quiet {out}")

speak("Hello, I am Trimind AI. Your conference room is ready.")
