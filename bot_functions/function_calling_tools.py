import requests
import bot_functions.other_functions.distress 
import bot_functions.games.adventure_game_test
import sensitiveData


def distress():
    #distress.main()
    distress.main()
    #Example string for testing
    print("Informing Parents...")

def game():
    #adventure_game_test.main()
    
    #Example string for testing
    print("Playing Game...")


def get_chatgpt_function_choice(input_text):
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = sensitiveData.apiKey

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
                        "location": {
                            "type": "string",
                            "description": "Example return",
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
    get_chatgpt_function_choice('I want to play a game')
    
# Call the main function
main()


