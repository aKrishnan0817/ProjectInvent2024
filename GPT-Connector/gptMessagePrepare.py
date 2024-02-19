import os
import sys
from openai import OpenAI
from toolkit.tools import tools
from TTS import ttsPlay
from speech_to_text import speech_to_text


sys.path.append('../')
import sensitiveData

API_KEY = sensitiveData.apiKey
client = OpenAI(api_key=API_KEY)

#inputType 1 for text, 0 for speech
def prepare_message(iprompt,inputType, functionCalling = tools):
  #enter the request with a microphone or type it if you wish
  if inputType == 2:
      uinput = ""
  elif inputType:
      print("Enter a request and press ENTER:")
      uinput = input("")
      iprompt.append({"role": "user", "content": uinput})
  else:
      uinput = speech_to_text()
      iprompt.append({"role": "user", "content": uinput})




  response=client.chat.completions.create(model="gpt-4",messages=iprompt,tools=functionCalling, tool_choice="auto" ) #ChatGPT dialo


  text = response.choices[0].message.content
  try:
      functionCalled = response.choices[0].message.tool_calls[0].function.name
      #response=client.chat.completions.create(model="gpt-4",messages=iprompt)
  except:
      functionCalled = None
      ttsPlay(text)

  return iprompt, text, functionCalled


if __name__ == "__main__":
    iprompt = []
    assert1={"role": "system", "content": "You are a frined of a nine year old boy"}
    assert2={"role": "assistant", "content": "You are to act and talk the way a younger child would to his friends"}
    iprompt.append(assert1)
    iprompt.append(assert2)
    iprompt,text,functionCalled=prepare_message(iprompt,1) #preparing the messages for ChatGPT
    print("Function called:", functionCalled)
    print("ChatGPT response:",text)
