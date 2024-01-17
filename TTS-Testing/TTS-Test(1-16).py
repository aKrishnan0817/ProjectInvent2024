import speech_recognition as sr
from openai import OpenAI


import sys
sys.path.append('/')
import sensitiveData

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=10)  # Record audio for up to 10 seconds

    try:
        print("Transcribing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Error connecting to Google API: {e}")

if __name__ == "__main__":
    speech_to_text()
