import requests
import other_functions.distress 
import games.adventure_game


def distress():
    distress.main()

def game():
    adventure_game.main()

def perform_calculation():
    print("Performing calculation...")

def get_chatgpt_function_choice(input_text):
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = "" #NEVER UPDATE TO GITHUB


    tools = [
        {
            "type": "function",
            "function": {
                "name": "perform_calculation",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        }
    ]
    
    payload = {
        "model": "gpt-3.5-turbo",
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

# Main function to handle input and call appropriate function
def main():
    get_chatgpt_function_choice('Please calculate this: 2 + 2')

    #example things that jonah might say and its corresponding fucntion
    messages_from_jonah = {"I'm feeling very nervous and scared. What should I do?": 'distress', "I want to play a game" : "game"}
# Call the main function
main()


