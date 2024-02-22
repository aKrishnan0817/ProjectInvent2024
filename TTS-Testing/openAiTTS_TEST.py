from openai import OpenAI
import sys
sys.path.append('../')
import pygame
import sensitiveData
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

API_KEY = sensitiveData.apiKey
client = OpenAI(api_key=API_KEY)

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Atuls First Open ai TEst",
)
response.stream_to_file("output.mp3")

def play_audio(audio_file):
    # Initialize pygame
    pygame.init()
    # Load the audio file
    pygame.mixer.music.load(audio_file)
    # Play the audio file
    pygame.mixer.music.play()
    # Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        continue

    print("--finished")

if __name__ == "__main__":
    play_audio("output.mp3")
