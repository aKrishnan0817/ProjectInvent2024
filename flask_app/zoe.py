def get_zoe_bot_response(client, **kwargs):
    system = kwargs["system"]
    chat_history = kwargs["chat_history"]
    user_input = kwargs["user_input"]
    output = client.chat.completions.create(model="gpt-3.5-turbo-0301",
                                            temperature=1,
                                            presence_penalty=0,
                                            frequency_penalty=0,
                                            max_tokens=2000,
                                            messages=[
                                                {"role": "system", "content": f"{system}. Conversation history: {chat_history}"},
                                                {"role": "user", "content": f"{user_input}"},
                                            ])

    chatgpt_output = ""
    if output.choices:
        # Accessing the content attribute directly
        chatgpt_output = output.choices[0].message.content

    return chatgpt_output

