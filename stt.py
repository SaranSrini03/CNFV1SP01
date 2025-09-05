from dotenv import load_dotenv
import os
import speech_recognition as sr
import datetime
import sys
from pathlib import Path
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a valid model name, e.g.:
model = genai.GenerativeModel("gemini-2.5-pro")

recognizer = sr.Recognizer()

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ask_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()

print("🎤 Voice Assistant with Gemini Started")
print("Adjusting to background noise...")

desktop = Path.home() / "Desktop"

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Ready! Speak something...")

    while True:
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower().strip()
            line = f"[{get_timestamp()}] {text}"
            print(line)

            # Save transcript
            with open("transcript.txt", "a", encoding="utf-8") as f:
                f.write(line + "\n")

            # Voice stop
            if "goodbye" in text:
                print("🛑 Stop command detected. Exiting...")
                break

            # Send to Gemini for interpretation
            instruction = ask_gemini(
                f"You are a voice assistant. User said: '{text}'. "
                "If it's a command, explain in one line what to do (like 'create file on desktop'). "
                "If it's small talk, just respond politely."
            )
            print(f"Fuse : {instruction}")

            if "create file" in instruction.lower() or "create txt" in instruction.lower():
                file_path = desktop / "voice_note.txt"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("This is a file created by voice + Gemini.\n")
                print(f"📄 File created: {file_path}")

        except sr.UnknownValueError:
            print(f"[{get_timestamp()}] (Could not understand audio)")
        except sr.RequestError as e:
            print(f"[{get_timestamp()}] API unavailable: {e}")
            break
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user (Ctrl+C)")
            sys.exit(0)
