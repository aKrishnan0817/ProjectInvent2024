import elevenlabs
import os
import sys

sys.path.append('../')
import sensitiveData

TTSapiKey=sensitiveData.TTSapiKey

elevenlabs.set_api_key(TTSapiKey)

def ttsPlay(text):
    voice = elevenlabs.Voice(
        voice_id = "eXc59clrDTZyQAX35P0w",
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
