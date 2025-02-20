import os
import sys

import pygame
from openai import OpenAI

sys.path.append('../')
import sensitiveData
import warnings

API_KEY = sensitiveData.apiKey
client = OpenAI(api_key=API_KEY)


def play_audio(audio_file):
    # Initialize pygame
    try:
        pygame.init()
        # Load the audio file
        pygame.mixer.music.load(audio_file)
        # Play the audio file
        pygame.mixer.music.play()
        # Wait until the music finishes playing
        while pygame.mixer.music.get_busy():
            continue
    except:
        print("")


def ttsPlay(text):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    response.stream_to_file("gptOutput.mp3")

    play_audio("gptOutput.mp3")

    os.remove("gptOutput.mp3")
