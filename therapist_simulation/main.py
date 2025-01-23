from owlbotAgent import OwlbotAgent
from childAgent import ChildAgent
from sensitiveData import apiKey
import time


openAI_api_key = apiKey

def main():
    owlbot = OwlbotAgent(model="gpt-4o-mini-2024-07-18", api_key=openAI_api_key)
    child = ChildAgent(model="gpt-4o-mini-2024-07-18", api_key=openAI_api_key)

    owlbot.set_modelParams(max_tokens=100, presence_penalty=0.3, temperature=0.5)
    child.set_modelParams(max_tokens=100, presence_penalty=0.3, temperature=0.5)


    initial_message = "I miss my mom"
    print(f"Child: {initial_message}")

    child.add_to_history(agent="child", input=initial_message)
    owlbot.add_to_history(agent="child", input=initial_message)

    owlbot_response = owlbot.get_response(initial_message)
    owlbot.add_to_history(agent="owlbot", input=owlbot_response)
    child.add_to_history(agent="owlbot", input=owlbot_response)
    print(f"Owlbot Response: {owlbot_response}")


    while True:
        child_response = child.get_response(owlbot_response)
        child.add_to_history(agent="child", input=child_response)
        owlbot.add_to_history(agent="child", input=child_response)
        print(f"Child Response: {child_response}")


        owlbot_response = owlbot.get_response(child_response)
        owlbot.add_to_history(agent="owlbot", input=owlbot_response)
        child.add_to_history(agent="owlbot", input=owlbot_response)
        print(f"Owlbot Response: {owlbot_response}")

if __name__ == "__main__":
    main()