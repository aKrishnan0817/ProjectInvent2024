import requests

def get_j_bot_response(client, **kwargs):
    #system = kwargs["system"]
    #chat_history = kwargs["chat_history"]
    user_input = kwargs["user_input"]
    return get_chatgpt_function_choice(user_input)
    #output = client.chat.completions.create(model="gpt-3.5-turbo-0301",
    #                                        temperature=1,
    #                                        presence_penalty=0,
    #                                        frequency_penalty=0,
    #                                        max_tokens=2000,
    #                                        messages=[
    #                                            {"role": "system", "content": f"{system}. Conversation history: {chat_history}"},
    #                                            {"role": "user", "content": f"{user_input}"},
    #                                        ])

    #chatgpt_output = ""
    #if output.choices:
    #    # Accessing the content attribute directly
    #    chatgpt_output = output.choices[0].message.content

    #return chatgpt_output

def get_chatgpt_function_choice(input_text):
    print("running get_chatgpt_function_choice")
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = "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"

    #Define tools, commented-out attributes are not used by example but could be useful for the actual functionality
    tools = [
        {
            "type": "function",
            "function": {
                "name": "distress",
                "description": "notify caregivers that user is distressed. This should only be used in extreme cases",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "reason for the notification",
                        },
                        #"unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },

                    #"required": ["location"],
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
                "name": "relaxation_script",
                "description": "writes a relaxation script to be read to user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "background_sounds": {
                            "type": "string",
                            "description": "audio file to be played while reading script",
                            "enum": ["water", "wind", "none"]
                        },
                        "sentence1": {
                            "type": "string",
                            "description": "first sentence of relaxation script"
                        },
                        "wait_time1": {
                            "type": "string",
                            "description": "number of seconds to wait after reading first sentence of script"
                        },
                        "sentence2": {
                            "type": "string",
                            "description": "second sentence of relaxation script"
                        },
                        "wait_time2": {
                            "type": "string",
                            "description": "number of seconds to wait after reading second sentence of script"
                        },
                    },
                },
            }
        }
    ]

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": input_text}
        ],
        "tools": tools,
        "tool_choice": "auto"
    }

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response_data = response.json()
    print(response)
    print(response_data)
    return response_data