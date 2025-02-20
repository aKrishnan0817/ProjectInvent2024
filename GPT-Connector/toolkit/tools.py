from prompts import promptList, version

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
            "description": promptList[version]["psyschoeducationPrompt"],
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
    }

]
