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
        
        # Process the emotion data if the record_emotion_intensity function was called
        if func == "record_emotion_intensity" and emotion:
            try:
                import json
                print("Raw emotion data:", emotion)
                # Try to parse the emotion data
                emotion_data = json.loads(emotion)
                print("Parsed emotion data:", emotion_data)
                
                if "emotion" in emotion_data and "rating" in emotion_data:
                    # Log the emotion to the website
                    context_note = emotion_data.get("context", "Self Reported During Session")
                    child.log_emotion(emotion_data["emotion"], emotion_data["rating"], context_note)
                    print(f"Logged emotion: {emotion_data['emotion']} with intensity {emotion_data['rating']} to website")
                    
                    # Respond to the user
                    response = emotion_data.get("convo", "Thank you for sharing how you feel.")
                    print("OWL response:", response)
                    ttsPlay(response)
                else:
                    print("Missing required fields in emotion data.")
                    print("Available keys:", list(emotion_data.keys()))
            except Exception as e:
                print(f"Error processing emotion data: {e}")
                print(f"Type of emotion data: {type(emotion)}")
                print(f"Raw emotion data: {emotion}")
                
        if func in ["story", "stop", "distress", "coping", "game"]:
            return func
