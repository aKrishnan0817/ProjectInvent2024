import sys
sys.path.append('../')

from prompts import promptList, version
EMOTIONS = ["Anxious", "Happy", "Angry", "Calm", "Sad"]
tools = [
    {
        "type": "function",
        "function": {
            "name": "distress",
            "description": promptList[version]["distressPrompt"],
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                    # "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },

                # "required": ["location"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "story",
            "description": "the user wants to listen to a story",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                    # "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },

                # "required": ["location"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "game",
            "description": "plays a game with the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                },
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "stop",
            "description": "the user wants to stop having this conversation",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                },
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "coping",
            "description": promptList[version]["copingPrompt"],
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                },
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "psychoeducation",
            "description": promptList[version]["psychoeducationPrompt"],
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                },
            },
        }
    },
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
