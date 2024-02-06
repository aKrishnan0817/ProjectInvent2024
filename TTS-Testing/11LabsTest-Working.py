import os
import sys

import elevenlabs


sys.path.append('../')
import sensitiveData
import requests

TTSapiKey=sensitiveData.TTSapiKey
import elevenlabs

'''elevenlabs.set_api_key(TTSapiKey)

voice = elevenlabs.Voice(
    voice_id = "MBl73QmiIEX1OVzDjkjN",
    settings = elevenlabs.VoiceSettings(
        stability = 0,
        similarity_boost = 0.75
    )
)

audio = elevenlabs.generate(
    text= "Try me... Make my day.",
    voice = voice
)'''

audio = elevenlabs.generate(
    text = "Hi, I love microwaving honey buns",
    voice = "Adam"
)

elevenlabs.play(audio)
elevenlabs.save(audio, "HoneyBuns.mp3")
