from openai import OpenAI

#from gtts import gTTS
import os
import sys
import elevenlabs
import speech_recognition as sr



sys.path.append('../')
import sensitiveData

API_KEY = sensitiveData.apiKey
TTSapiKey=sensitiveData.TTSapiKey



os.environ['OPENAI_API_KEY'] =API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=10)  # Record audio for up to 10 seconds

    try:
        print("Transcribing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Error connecting to Google API: {e}")


#Speech to text. Use OS speech-to-text app. For example,   Windows: press Windows Key + H
iprompt = []
assert1={"role": "system", "content": "You are a helpful assistant."}
assert2={"role": "assistant", "content": "Geography is an important topic if you are going on a once in a lifetime trip."}
iprompt.append(assert1)
iprompt.append(assert2)

def prepare_message(iprompt):
  #enter the request with a microphone or type it if you wish

  uinput= speech_to_text()
  '''print("Enter a request and press ENTER:")
  uinput = input("")'''



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

    response=client.chat.completions.create(model="gpt-4",messages=iprompt) #ChatGPT dialog

    text = response.choices[0].message.content


    print("ChatGPT response:",text)

    elevenlabs.set_api_key(TTSapiKey)

    voice = elevenlabs.Voice(
        voice_id = "MBl73QmiIEX1OVzDjkjN",
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
