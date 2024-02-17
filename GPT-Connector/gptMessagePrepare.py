import os
import sys
from openai import OpenAI
import tools
from TTS import ttsPlay
from speech_to_text import speech_to_text


sys.path.append('../')
import sensitiveData

API_KEY = sensitiveData.apiKey
client = OpenAI(api_key=API_KEY)

#inputType 1 for text, 0 for speech
def prepare_message(iprompt,inputType, functionCalling = tools.tools):
  #enter the request with a microphone or type it if you wish
  if inputType:
      print("Enter a request and press ENTER:")
      uinput = input("")
  else:
      uinput = speech_to_text()

  iprompt.append({"role": "user", "content": uinput})

  response=client.chat.completions.create(model="gpt-4",messages=iprompt,tools=functionCalling, tool_choice="auto" ) #ChatGPT dialog
  text = response.choices[0].message.content

  try:
      functionCalled = response.choices[0].message.tool_calls[0].function.name
      #response=client.chat.completions.create(model="gpt-4",messages=iprompt)
  except:
      functionCalled = None
      ttsPlay(text)

  return iprompt, text, functionCalled
