import os
import sys

import speech_recognition as sr
from langdetect import detect
from openai import OpenAI

sys.path.append('../')
import sensitiveData

API_KEY = sensitiveData.apiKey
client = OpenAI(api_key=API_KEY)
from TTS import ttsPlay
from piComponents import piComponents

try:
    from gpiozero import Button
    import RPi.GPIO as GPIO
except:
    print("")


def speech_to_text(button):
    text = None
    while text == None or detect(text) != "en":

        getSpeech(button)
        try:
            print("Transcribing...")
            audio_file = open("audio_file.wav", "rb")
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            text = transcription.text
            # print(text)
            # print(detect(text))
            nonEn = False
            try:
                nonEn = detect(text) in ["ko", "zh-cn", "zh-tw", "ja", "th", "vi"]
            except:
                print("")
            if text == None or nonEn:
                print("OWL response: I apologize but can you please repeat that")
                ttsPlay("I apologize but can you please repeat that")
                continue
            print("You said:", text)
            os.remove("audio_file.wav")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio. Try Again")
            os.remove("audio_file.wav")
        except sr.RequestError as e:
            print(f"Error connecting to Google API: {e}")
            os.remove("audio_file.wav")
    return None


def getSpeech(button):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        if button.getButtonUse():
            # Wait for button press
            while not button.checkButtonPress():
                time.sleep(0.1)  # Small delay to avoid CPU hogging
            # Button is now pressed, LED is on
            try:
                print("Listening...")
                # Set a timeout that's longer than expected button press
                audio = recognizer.listen(source, timeout=30)
            except:
                print("couldn't listen")
                button.setLed(0)  # Ensure LED is off
                return None
            # Turn off LED when done
            button.setLed(0)
        else:
            print("using mic with no button")
            audio = recognizer.listen(source, timeout=10)
    try:
        with open("audio_file.wav", "wb") as file:
            file.write(audio.get_wav_data())
        return "audio_file.wav"
    except:
        print("couldnt write audio file")
        return None

if __name__ == "__main__":
    button = piComponents(buttonPin=2, ledPin=4)
    speech_to_text(button)
