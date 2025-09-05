import speech_recognition as sr
import datetime
import sys

# Create recognizer instance
recognizer = sr.Recognizer()

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("🎤 Voice to Text Started")
print("Adjusting to background noise...")

# Use default system microphone
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Ready! Speak something... (say 'hey echo stop' or press Ctrl+C to quit)")

    while True:
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower().strip()  # normalize text
            line = f"[{get_timestamp()}] {text}"
            print(line)

            # Save transcript
            with open("transcript.txt", "a", encoding="utf-8") as f:
                f.write(line + "\n")

            # Voice stop command
            if "green apple" in text:
                print("🛑 Stop command detected. Exiting...")
                break

        except sr.UnknownValueError:
            print(f"[{get_timestamp()}] (Could not understand audio)")
        except sr.RequestError as e:
            print(f"[{get_timestamp()}] API unavailable: {e}")
            break
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user (Ctrl+C)")
            sys.exit(0)
