import speech_recognition as sr

import sys
from openai import OpenAI
import os
import time
sys.path.append('../')
import sensitiveData
API_KEY = sensitiveData.apiKey
client = OpenAI(api_key=API_KEY)

from piComponents import piComponents

try:
    from gpiozero import Button
    import RPi.GPIO as GPIO
except:
    print("")

def speech_to_text(button):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        if button.getButtonUse():
            if button.checkButtonPress():
                try:
                    audio = recognizer.listen(source, timeout=4)# Record audio for up to 4 seconds
                except:
                    print("couldnt listen")
            else:
                GPIO.output(4,GPIO.LOW)
        else:
            audio = recognizer.listen(source, timeout=4)
    if button.getButtonUse():
        GPIO.output(4,GPIO.LOW)
    with open("audio_file.wav", "wb") as file:
        file.write(audio.get_wav_data())

    text = None
    while text == None:
        try:
            print("Transcribing...")
            audio_file = open("audio_file.wav", "rb")
            transcription = client.audio.transcriptions.create(
              model="whisper-1",
              file=audio_file
            )
            text=transcription.text
            print("You said:", text)
            os.remove("audio_file.wav")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio. Try Again")
            os.remove("audio_file.wav")
        except sr.RequestError as e:
            print(f"Error connecting to Google API: {e}")
            os.remove("audio_file.wav")
            break
