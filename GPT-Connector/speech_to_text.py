import atexit
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
except Exception as e:
    raise Exception("GPIO libraries not available: " + str(e))


recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index=1)

# ---- permanently open the PortAudio stream ----
print("Binding PortAudio stream to microphone...")
live_source = microphone.__enter__()
atexit.register(microphone.__exit__, None, None, None)

CALIBRATION_TIME = 1
print("Calibrating mic for", CALIBRATION_TIME, "s …")
recognizer.adjust_for_ambient_noise(live_source, duration=CALIBRATION_TIME)
recognizer.dynamic_energy_threshold = False
print("Energy threshold locked at", recognizer.energy_threshold)
recognizer.pause_threshold       = 1.5
recognizer.non_speaking_duration = 0.3



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
    #print("?1 Is the microphone listening now?")
    print("Say something...")
    if button.getButtonUse():
        print("Waiting for button press …")
        button.button.wait_for_press()

        try:
            print("Listening...")
            button.setLed(1)
            audio = recognizer.listen(live_source, timeout=15, phrase_time_limit=None)
        except sr.WaitTimeoutError:
            print("Nothing heard within 15 s")
            audio = None
        finally:
            button.setLed(0)

        if not audio:
            return None
    else:
        print("using mic with no button")
        audio = recognizer.listen(live_source, timeout=15, phrase_time_limit=None)

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
