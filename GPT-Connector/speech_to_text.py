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


def getSpeech(button):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        if button.getButtonUse():
            if button.checkButtonPress():
                try:
                    audio = recognizer.listen(source, timeout=10)  # Record audio for up to 4 seconds
                except:
                    print("couldnt listen")
            else:
                GPIO.output(4, GPIO.LOW)
        else:
            print("using mic with no button")
            audio = recognizer.listen(source, timeout=10)
    if button.getButtonUse():
        GPIO.output(4, GPIO.LOW)
    try:
        with open("audio_file.wav", "wb") as file:
            file.write(audio.get_wav_data())
        return "audio_file.wav"
    except:
        print("couldnt write audio file")
        return None
