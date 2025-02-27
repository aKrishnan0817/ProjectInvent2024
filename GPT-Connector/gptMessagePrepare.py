import sys

sys.path.append('/Users/jphillips/ProjectInvent2024')
from time import time

from openai import OpenAI
import base64

from TTS import ttsPlay, play_audio
from speech_to_text import speech_to_text, getSpeech
from toolkit.tools import tools
from toolkit.noTools import noTools

MODEL = "gpt-4o-audio"

def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func


sys.path.append('../')
import sensitiveData

API_KEY = sensitiveData.apiKey
client = OpenAI(api_key=API_KEY)


# inputType 1 for text, 0 for speech
def prepare_message(iprompt, inputType, functionCalling=tools, button=None):
    text = None
    response = None
    functionCalled = None

    # enter the request with a microphone or type it if you wish
    if inputType == 2:
        uinput = ""
    elif inputType:
        print("Enter a request and press ENTER:")
        uinput = input("")
        iprompt.append({"role": "user", "content": uinput})
    else:
        if MODEL == "gpt-4o":
            uinput = timer_func(speech_to_text)(button)
            iprompt.append({"role": "user", "content": uinput})
            response = timer_func(client.chat.completions.create)(model="gpt-4o", messages=iprompt, tools=noTools,
                                                              tool_choice="auto")
            text = response.choices[0].message.content
            try:
                functionCalled = response.choices[0].message.tool_calls[0].function.name
                print("Function called:", functionCalled)

                # response=client.chat.completions.create(model="gpt-4",messages=iprompt)
            except:
                functionCalled = None
                print("OWL response:", text)
                iprompt.append({"role": "assistant", "content": text})
                timer_func(ttsPlay)(text)
        else:
            audio_path = timer_func(getSpeech)(button)
            if not audio_path:
                return iprompt, "Failed to get audio input.", None

            try:
                # Open audio file in binary mode
                with open("audio_file.wav", "rb") as audio_file:
                    # Add audio message to the prompt
                    iprompt.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Processing audio input"
                            },{
                                "type": "input_audio",
                                "input_audio": {
                                    "data": base64.b64encode(audio_file.read()).decode('utf-8'),
                                    "format": "wav"
                                }
                            }
                        ]
                    })

                response = timer_func(client.chat.completions.create)(
                    model="gpt-4o-audio-preview",
                    messages=iprompt,
                    modalities=["text", "audio"],
                    #response_format={"type": "text"},  # Use "text" as it's supported
                    audio={"voice": "alloy", "format": "wav"}
                    #response_format={"type": "audio_text"}
                    )

                print(response.choices[0].message)
                # Get text response
                text = response.choices[0].message.content

                        # If there's audio in the response
                if hasattr(response.choices[0].message, 'audio'):
                            wav_bytes = base64.b64decode(response.choices[0].message.audio.data)
                            text = response.choices[0].message.audio.transcript
                            with open("output_audio.wav", "wb") as f:
                                f.write(wav_bytes)
                            play_audio("output_audio.wav")

            except Exception as e:
                print(f"Error processing audio: {e}")
                return iprompt, f"Error: {str(e)}", None
            #wav_bytes = base64.b64decode(response.choices[0].message.audio.data)
            #with open("output_audio.wav", "wb") as f:
            #    f.write(wav_bytes)
            #    play_audio(f)

    try:
        functionCalled = response.choices[0].message.tool_calls[0].function.name
        print("Function called:", functionCalled)

        # response=client.chat.completions.create(model="gpt-4",messages=iprompt)
    except:
        functionCalled = None
        print("OWL response:", text)
        iprompt.append({"role": "assistant", "content": text})



    return iprompt, text, functionCalled


def moderateMessage(text, uinput):
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

    censor_response = client.chat.completions.create(model="gpt-4o", messages=mod_message)
    # print(censor_response)
    censor = censor_response.choices[0].message.content

    return censor


if __name__ == "__main__":
    iprompt = []
    assert1 = {"role": "system", "content": "You are a friend of a nine year old boy"}
    assert2 = {"role": "assistant", "content": "You are to act and talk the way a younger child would to his friends"}
    iprompt.append(assert1)
    iprompt.append(assert2)
    iprompt, text, functionCalled = prepare_message(iprompt, 1)  # preparing the messages for ChatGPT
    print("Function called:", functionCalled)
    print("ChatGPT response:", text)
