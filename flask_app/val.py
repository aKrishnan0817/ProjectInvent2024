import requests

def get_val_bot_response(client, **kwargs):
    #system = kwargs["system"]
    #chat_history = kwargs["chat_history"]
    user_input = kwargs["user_input"]
    return get_chatgpt_function_choice(user_input, client)
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

def get_chatgpt_function_choice(input_text, client):
    print("running get_chatgpt_function_choice")
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = client.api_key

    #Define tools, commented-out attributes are not used by example but could be useful for the actual functionality
    tools = [
        {
            "type": "function",
            "function": {
                "name": "distress",
                "description": "notify caregivers that user is distressed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_message": {
                            "type": "string",
                            "description": "a message for the caregivers",
                        },
                        "child_message": {
                            "type": "string",
                            "description": "a message for the child",
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
                "name": "thinking_trap",
                "description": "identify thinking traps",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_message": {
                            "type": "string",
                            "description": "a message for the caregivers",
                        },
                        "thinking_trap": {
                            "type": "string",
                            "description": "common ways of thinking that are not helpful",
                            "enum": ["black and white thinking", "over generalization","filtering" ]
                        },
                        "child_message": {
                            "type": "string",
                            "description": "a message for the child",
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