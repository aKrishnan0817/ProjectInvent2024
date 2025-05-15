import sys

sys.path.append('/Users/jphillips/ProjectInvent2024')
from time import time

from openai import OpenAI
import base64
import copy
from TTS import ttsPlay, play_audio
from speech_to_text import speech_to_text, getSpeech
from toolkit.tools import tools
from toolkit.noTools import noTools
import json

MODEL = "gpt-4o"

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
            response = timer_func(client.chat.completions.create)(model="gpt-4o", messages=iprompt, tools=functionCalling,
                                                              tool_choice="auto")
            text = response.choices[0].message.content
            try:
                if response.choices[0].message.tool_calls:
                    functionCalled = response.choices[0].message.tool_calls[0].function.name
                    print("Function called:", functionCalled)
                    
                    # Extract the function arguments as JSON string
                    function_args = response.choices[0].message.tool_calls[0].function.arguments
                    print("Function arguments:", function_args)
                    
                    # Set up assistant message with tool call
                    tool_call = response.choices[0].message.tool_calls[0]
                    tool_call_id = tool_call.id
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    iprompt.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": tool_call_id,
                            "type": "function",
                            "function": {
                                "name": function_name,
                                "arguments": json.dumps(function_args)
                            }
                        }]
                    })

                    # Run the corresponding tool function
                    if functionCalling and function_name in functionCalling:
                        try:
                            tool_func = functionCalling[function_name]
                            tool_result = tool_func(**function_args)
                            tool_response = json.dumps(tool_result) if not isinstance(tool_result, str) else tool_result
                        except Exception as e:
                            tool_response = f"Error executing tool: {str(e)}"
                    else:
                        tool_response = f"No such tool: {function_name}"

                    # Add tool response message
                    iprompt.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": tool_response
                    })

                    # Make second call to get final assistant message
                    response2 = timer_func(client.chat.completions.create)(
                        model=MODEL,
                        messages=iprompt
                    )

                    final_reply = response2.choices[0].message.content
                    iprompt.append({"role": "assistant", "content": final_reply})
                    text = final_reply
                else:
                    functionCalled = None
                    print("OWL response:", text)
                    iprompt.append({"role": "assistant", "content": text})
                    timer_func(ttsPlay)(text)
            except Exception as e:
                print(f"Error processing function call: {e}")
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

                audio_request = "Please respond in a conversational manner and always provide an audio response when possible."

                if iprompt and len(iprompt) > 0:
                    if iprompt[0]["role"] == "system":
                        # Check if the audio request is already included
                        if audio_request not in iprompt[0]["content"]:
                            iprompt[0]["content"] += " " + audio_request
                    else:
                        # Insert a new system prompt that includes both psychoeducation and audio request
                        iprompt.insert(0, {"role": "system", "content": systemPsychoeducationPrompt + " " + audio_request})
                else:
                    # Create a new system prompt if iprompt is empty
                    iprompt = [{"role": "system", "content": systemPsychoeducationPrompt + " " + audio_request}]


                print("iprompt length")
                print(len(iprompt))
                response = timer_func(client.chat.completions.create)(
                    model="gpt-4o-audio-preview",
                    messages=iprompt,
                    modalities=["text", "audio"],
                    audio={"voice": "alloy", "format": "wav"},
                    #response_format={"type": "json_object"}
                    )

                message = response.choices[0].message

                # Print top-level keys in the response
                print("Top-level keys in response:", list(response.__dict__.keys()))

                # Ensure there are choices before accessing
                if response.choices and len(response.choices) > 0:
                    print("Top-level keys in response.choices[0]:", list(response.choices[0].__dict__.keys()))
                else:
                    print("No choices found in response.")    

                # Convert the message object to a dictionary
                message_dict = copy.deepcopy(message.__dict__)

                # If 'audio' exists, remove its 'data' field
                if "audio" in message_dict and message_dict["audio"]:
                    message_dict["audio"] = {
                        "id": message_dict["audio"].id,
                        "expires_at": message_dict["audio"].expires_at,
                        "transcript": message_dict["audio"].transcript
                    }

                # Print the filtered message dictionary
                print(message_dict)
                # Get text response
                text = response.choices[0].message.content

                if hasattr(response.choices[0].message, 'audio') and response.choices[0].message.audio:
                    wav_bytes = base64.b64decode(response.choices[0].message.audio.data)
                    text = response.choices[0].message.audio.transcript
                    with open("output_audio.wav", "wb") as f:
                        f.write(wav_bytes)
                    play_audio("output_audio.wav")
                else:
                    print("No audio in response, falling back to text.")
                    text = response.choices[0].message.content  # Ensure text is always captured
                    timer_func(ttsPlay)(text)


            except Exception as e:
                print(f"Error processing audio: {e}")
                return iprompt, f"Error: {str(e)}", None
            #wav_bytes = base64.b64decode(response.choices[0].message.audio.data)
            #with open("output_audio.wav", "wb") as f:
            #    f.write(wav_bytes)
            #    play_audio(f)

    try:
        if response and response.choices and response.choices[0].message.tool_calls:
            functionCalled = response.choices[0].message.tool_calls[0].function.name
            print("Function called:", functionCalled)
            
            # Extract the function arguments as JSON string
            function_args = response.choices[0].message.tool_calls[0].function.arguments
            print("Function arguments:", function_args)
            
            # Set text to the function arguments string for further processing
            text = function_args
            
            # Add the assistant's response to the prompt if not already added
            if len(iprompt) == 0 or iprompt[-1]["role"] != "assistant":
                iprompt.append({
                    "role": "assistant", 
                    "content": None,
                    "tool_calls": [{
                        "id": response.choices[0].message.tool_calls[0].id,
                        "type": "function",
                        "function": {
                            "name": functionCalled,
                            "arguments": function_args
                        }
                    }]
                })
        else:
            functionCalled = None
            print("OWL response:", text)
            if text and (len(iprompt) == 0 or iprompt[-1]["role"] != "assistant"):
                iprompt.append({"role": "assistant", "content": text})
    except Exception as e:
        print(f"Error processing function call: {e}")
        functionCalled = None
        print("OWL response:", text)
        if text and (len(iprompt) == 0 or iprompt[-1]["role"] != "assistant"):
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
