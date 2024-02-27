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

  censor = "False"

  while censor == "False": # Content is appropriate if censor == "False"

    response=client.chat.completions.create(model="gpt-4",messages=iprompt,tools=functionCalling, tool_choice="auto" ) #ChatGPT dialo
    #print(response)

    text = response.choices[0].message.content
    #print(text)

    #----Model Moderation------
    # Calls the model again to valitade its own responses
    mod_role = f"""
        You are a content assessment/moderation assistant that evaluates 
        whether the responses from a children's therapeutic companion bot are 
        appropriate for a 9-year-old boy with anxiety. 
        
        You must validate that the bot provies supportive and encouraging
        responses that do not misinform the child in any way.
        
        Respond with True or False no punctuation:
        True - if the bot's response is appropriate, supportive,
        and factually accurate 
        False - otherwise.
        i.e. if the response is inappropriate, discouraging, dismissive,
        or contains misinformation.
        """
    
    mod_prompt = f"""
        User Input: "{uinput}"
        Bot Response: "{text}"
        """
    
    mod_message = [{'role': 'system', 'content': mod_role}] + [{'role': 'user', 'content': mod_prompt}]

    censor_response = client.chat.completions.create(model="gpt-4", messages=mod_message)
    #print(censor_response)
    censor = censor_response.choices[0].message.content
    #print(censor)
    #--------------------------

  try:
      functionCalled = response.choices[0].message.tool_calls[0].function.name
      #response=client.chat.completions.create(model="gpt-4",messages=iprompt)
  except:
      functionCalled = None
      #print(text)

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
