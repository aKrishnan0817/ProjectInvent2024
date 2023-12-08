from openai import OpenAI

import sys
sys.path.append('/')
import sensitiveData
client = OpenAI(api_key=sensitiveData.apiKey)


'''audio_file= open("audio.m4a", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file
)
print(transcript.text)'''



stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
