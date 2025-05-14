import random
import sys
import json
import toolkit.emotionTools as emotionTools
import sensitiveData
from WebsiteConnector.website_client import Client as WebsiteClient
sys.path.append('../')

from TTS import ttsPlay
from gptMessagePrepare import prepare_message

website_client = WebsiteClient(sensitiveData.website_credentials[0], sensitiveData.website_credentials[1])
print(f"Logged in as {website_client.username}")
child = website_client.list_children()[0]

def emotionTracking(inputType, button = None):
    message = "How are you today? Is there any specific emotion you are feeling right now?"
    print("OWL response:", message)
    ttsPlay(message)
    iprompt = []
    assert1 = {"role": "system", "content": f"you are an ai friend to a {child.age} child"}
    assert2 = {"role": "assistant", "content": emotionTools.SYSTEM_PROMPT}
    iprompt.append(assert1)
    iprompt.append(assert2)
    while True:
        iprompt, emotion, func = prepare_message(iprompt, inputType, emotionTools.emotionTool, button=button)
        print(emotion)
        print(func)
        if func in ["story", "stop", "distress", "coping", "game"]:
            return func
