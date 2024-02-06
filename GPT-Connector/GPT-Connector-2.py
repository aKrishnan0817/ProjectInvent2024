from openai import OpenAI

#from gtts import gTTS
import os
import sys
import elevenlabs
import speech_recognition as sr
import tools
from Game20questions import play20Questions
from TTS import ttsPlay


sys.path.append('../')
import sensitiveData

API_KEY = sensitiveData.apiKey
TTSapiKey=sensitiveData.TTSapiKey



os.environ['OPENAI_API_KEY'] =API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


#Speech to text. Use OS speech-to-text app. For example,   Windows: press Windows Key + H
iprompt = []
assert1={"role": "system", "content": "You are a frined of a nine year old boy"}
assert2={"role": "assistant", "content": "You are to act and talk the way a younger child would to his friends"}
iprompt.append(assert1)
iprompt.append(assert2)

def prepare_message(iprompt):
  #enter the request with a microphone or type it if you wish
  print("Enter a request and press ENTER:")
  uinput = input("")

  #preparing the prompt for OpenAI
  role="user"
  #prompt="Where is Tahiti located?" #maintenance or if you do not want to use a microphone
  line = {"role": role, "content": uinput}
  #creating the message

  assert3=line

  iprompt.append(assert3)
  return iprompt

#run the cell to start/continue a dialog

while(True):

    iprompt=prepare_message(iprompt) #preparing the messages for ChatGPT

    response=client.chat.completions.create(model="gpt-4",messages=iprompt,tools=tools.tools, tool_choice="auto" ) #ChatGPT dialog
    text = response.choices[0].message.content

    try:
        functionCalled = response.choices[0].message.tool_calls[0].function.name
        #response=client.chat.completions.create(model="gpt-4",messages=iprompt)
    except:
        functionCalled = None
        ttsPlay(text)

    print("Function called:", functionCalled)
    print("ChatGPT response:",text)


    if functionCalled == "game":
        response=client.chat.completions.create(model="gpt-4",messages=iprompt)
        print(response.choices[0].message.content)
        play20Questions(client)
