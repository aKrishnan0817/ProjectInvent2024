
import os
import sys

import elevenlabs


sys.path.append('../')
import sensitiveData
import requests

TTSapiKey=sensitiveData.TTSapiKey

CHUNK_SIZE = 1024

#voice id for old british guy i found (bad ass voice imo )
url = "https://api.elevenlabs.io/v1/text-to-speech/MBl73QmiIEX1OVzDjkjN"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": TTSapiKey
}

data = {
  "text": "Try me... Make my day.",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
#elevenlabs.play(response)

with open('output2.wav', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
