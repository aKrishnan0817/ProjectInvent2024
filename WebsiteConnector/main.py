import os
import json
import sensitiveData
from openai import OpenAI
from website_client import Client as WebsiteClient

client = OpenAI(api_key=sensitiveData.apiKey)
website_client = WebsiteClient(sensitiveData.website_credentials[0], sensitiveData.website_credentials[1])
child = website_client.list_children()[0]

EMOTIONS = ["Anxious", "Happy", "Angry", "Calm", "Sad"]
SYSTEM_PROMPT = f"""
You are an empathetic, context-aware assistant.  When the user’s message expresses or implies one of these emotions:
{EMOTIONS}

You should first ask them, in a warm, sensitive way, to rate the intensity on a 1–5 scale.
Once they reply with a number, you must call the function `record_emotion_intensity` with exactly four arguments: 
    `emotion` (the detected emotion), 
    `rating` (the integer 1–5), 
    'context' (a brief description of the context in the conversation), and 
    'convo' (your response to the user, to continue the conversation.).
Do not return any other text after calling the function.
If there’s no emotion, or the emotion is not present in the emotions list, just respond normally.
DO NOT assume the child's emotions, wait for them to report to you first. You CAN help them along by asking them what they are feeling, but do not assume anything.
"""

functions = [
    {
        "name": "record_emotion_intensity",
        "description": "Record the user's emotion and how intense it is from 1 to 5",
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
                    "maximum": 5,
                    "description": "User's self-reported intensity of the emotion"
                },
                "context": {
                    "type": "string",
                    "description": "A brief description of the context in the conversation."
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


def record_emotion_intensity(emotion: str, rating: int, context: str):
    child.log_emotion(emotion, rating, f'Self Reported During Session: {context}')
    return [emotion, rating, context]


def chat_with_emotion(history):
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
        functions=functions,
        function_call="auto",  # let the model decide when to call
        temperature=1,
        max_tokens=200
    )
    msg = resp.choices[0].message

    # If the model decided to call our function:
    if msg.function_call:
        # Parse out arguments
        args = json.loads(msg.function_call.arguments)
        emotion = args["emotion"]
        rating = args["rating"]
        context = args["context"]
        convo = args["convo"]

        # Call our Python function
        result = record_emotion_intensity(emotion, rating, context)

        # Finally, append the function call and its result to history
        history.append({
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": msg.function_call.name,
                "arguments": msg.function_call.arguments
            }
        })

        history.append({
            "role": "function",
            "name": msg.function_call.name,
            "content": json.dumps(result)
        })

        return result + [convo]

    else:
        # No function call: just regular assistant content
        history.append({"role": "assistant", "content": msg.content})
        return msg.content


if __name__ == "__main__":
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_text = input("You: ")
        history.append({"role": "user", "content": user_text})

        response = chat_with_emotion(history)

        if isinstance(response, list):
            print(f'\t[DEBUG] Logged: {response}')
            print("Assistant:", response[-1])
        else:
            print("Assistant:", response)
