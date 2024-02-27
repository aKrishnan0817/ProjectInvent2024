import requests
import distress
import games.adventure_game
import sys

sys.path.append('/')
import sensitiveData

# client = OpenAI(api_key=sensitiveData.apiKey)
apiKey = sensitiveData.apiKey


def distress():
    distress.main()


def game():
    games.adventure_game_test.main()


def perform_calculation():
    print("Performing calculation...")

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
    get_chatgpt_function_choice('Please calculate this: 2 + 2')

    # example things that jonah might say and its corresponding fucntion
    messages_from_jonah = {"I'm feeling very nervous and scared. What should I do?": 'distress',
                           "I want to play a game": "game"}
    
    #main loop - main in function calling should be the primary method that is always running, and can decide what to do from there. 
    while True:
        #placeholder
        return


# Call the main function

if __name__ == "__main__":
    main()
