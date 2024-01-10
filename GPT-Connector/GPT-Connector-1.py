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

def prepare_message():
  #enter the request with a microphone or type it if you wish
  # example: "Where is Tahiti located?"
  print("Enter a request and press ENTER:")
  uinput = input("")
  #preparing the prompt for OpenAI
  role="user"
  #prompt="Where is Tahiti located?" #maintenance or if you do not want to use a microphone
  line = {"role": role, "content": uinput}
  #creating the message
  assert1={"role": "system", "content": "You are a helpful assistant."}
  assert2={"role": "assistant", "content": "Geography is an important topic if you are going on a once in a lifetime trip."}
  assert3=line
  iprompt = []
  iprompt.append(assert1)
  iprompt.append(assert2)
  iprompt.append(assert3)
  return iprompt
while(True):
    iprompt = prepare_message()

    response=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=iprompt) #ChatGPT dialog

    text=response["choices"][0]["message"]["content"] #response in JSON

    print("ChatGPT response:",text)
