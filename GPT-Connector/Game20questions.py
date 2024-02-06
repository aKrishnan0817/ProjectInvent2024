
from openai import OpenAI
import random
from TTS import ttsPlay


def play20Questions(client):
    secretObjectType = random.choice(["animal", "plant", "inanimate object", "historical person"])
    secretObjectLetter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    secretObjectQuestion = "Choose a random example of a " + secretObjectType + ". It should start with the letter: " + secretObjectLetter + ". Your response should be a single word and nothing else. Do not tell the use what the object is unless explicity said so. Only respond yes or no."

    iprompt = []
    assert1={"role": "system", "content": "You are still waiting to decide what your secret object is."}
    assert2={"role": "assistant", "content": secretObjectQuestion}


    firstMessage = "Lets play 20 questions. I've thought of a word and you need to guess it."
    print(firstMessage)
    ttsPlay(firstMessage)

    iprompt.append(assert1)
    iprompt.append(assert2)

    while True:
        print("Write a guess and press ENTER:")
        uinput = input("")

        iprompt.append({"role": "user", "content": uinput})

        response=client.chat.completions.create(model="gpt-4",messages=iprompt)
        
        print("ChatGPT response:",response.choices[0].message.content)
        ttsPlay(response.choices[0].message.content)
