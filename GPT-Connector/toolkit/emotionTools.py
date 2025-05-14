import os
import sys
from toolkit.tools import tools
import sensitiveData
from WebsiteConnector.website_client import Client as WebsiteClient
import pandas as pd
website_client = WebsiteClient(sensitiveData.website_credentials[0], sensitiveData.website_credentials[1])
print(f"Logged in as {website_client.username}")
child = website_client.list_children()[0]


EMOTIONS = ["Anxious", "Happy", "Angry", "Calm", "Sad"]
SYSTEM_PROMPT = f"""
You are an empathetic, context-aware assistant.  
Your client is a {child.age}-year old named {child.name}. They started therapy on {child.start_date}.
When the user’s message expresses or implies one of these emotions:
{EMOTIONS}

You should first ask them, in a warm, sensitive way to the context of the conversation, to rate the intensity on a 1–10 scale.
DO NOT assume the child's emotions, wait for them to report to you first. You CAN help them along by asking them what they are feeling, but do not assume anything.
"""
emotionTool = [
    {
        "type": "function",
        "name": "record_emotion_intensity",
        "description": "Record the user's emotion, it's intensity, the context, and a follow-up response inside a JSON object.",
        "parameters": {
            "type": "object",
            "properties": {
                "emotion": {
                    "type": "string",
                    "enum": EMOTIONS
                },
                "rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 10,
                    "description": "User's self-reported intensity of the emotion. If given a word to describe the emotion, convert it to a number based on the intensity of the descriptor"
                },
                "context": {
                    "type": "string",
                    "description": "A brief description of the context of the conversation."
                },
                "convo": {
                    "type": "string",
                    "description": "A response to the user to continue the conversation. "
                }

            },
            "required": ["emotion", "rating", "context", "convo"]
        }
    }
]
emotionTool.append(tools[0])
emotionTool.append(tools[1])
emotionTool.append(tools[2])
emotionTool.append(tools[3])
emotionTool.append(tools[4])
emotionTool.append(tools[5])