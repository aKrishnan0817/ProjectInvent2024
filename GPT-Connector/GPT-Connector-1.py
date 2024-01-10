import openai
from gtts import gTTS
import os
import sys

sys.path.append('../')
import sensitiveData

API_KEY = sensitiveData.apiKey



os.environ['OPENAI_API_KEY'] =API_KEY

openai.api_key = os.getenv("OPENAI_API_KEY")

#Speech to text. Use OS speech-to-text app. For example,   Windows: press Windows Key + H
iprompt = []
assert1={"role": "system", "content": "You are a helpful assistant."}
assert2={"role": "assistant", "content": "Geography is an important topic if you are going on a once in a lifetime trip."}
iprompt.append(assert1)
iprompt.append(assert2)

def prepare_message(iprompt):
  #enter the request with a microphone or type it if you wish
  # example: "Where is Tahiti located?"
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

    response=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=iprompt) #ChatGPT dialog

    text=response["choices"][0]["message"]["content"] #response in JSON

    print("ChatGPT response:",text)
