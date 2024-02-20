import elevenlabs
import os
import sys

sys.path.append('../')
import sensitiveData

TTSapiKey=sensitiveData.TTSapiKey

elevenlabs.set_api_key(TTSapiKey)

def ttsPlay(text):
    voice = elevenlabs.Voice(
        voice_id = "tX8xKQjiAFQPJ7hI7ob1",
        settings = elevenlabs.VoiceSettings(
            stability = 0,
            similarity_boost = 0.75
        )
    )

    audio = elevenlabs.generate(
        text= text,
        voice = voice
    )

    elevenlabs.play(audio)
