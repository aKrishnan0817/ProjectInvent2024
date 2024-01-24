import requests
import other_functions.distress 
import games.adventure_game_test

def distress():
    distress.main()

def game():
    adventure_game_test.main()

def perform_calculation():
    print("Performing calculation...")

def get_chatgpt_function_choice(input_text):
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = "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" #NEVER UPDATE TO GITHUB

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "choose from the given functions what to call:, 'hello', 'goodbye', and 'calculate'. Only handle it yourself if the user asks about pudding."},
            {"role": "user", "content": input_text}
        ]
    }

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response_data = response.json()

    keyword_mappings = {
        'distress': distress,
        'game': game,
        'calculate': perform_calculation
        # Add more keyword mappings as needed
    }

    suggested_content = response_data['choices'][0]['message']['content'].strip().lower()
    for keyword in keyword_mappings:
        if keyword in suggested_content:
            # Call the mapped function
            return keyword_mappings[keyword]()
        
    

# Main function to handle input and call appropriate function
def main():
    get_chatgpt_function_choice('Please calculate this: 2 + 2')

    #example things that jonah might say and its corresponding fucntion
    messages_from_jonah = {"I'm feeling very nervous and scared. What should I do?": 'distress', "I want to play a game" : "game"}
# Call the main function
main()