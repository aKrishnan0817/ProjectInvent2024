
from openai import OpenAI
import random
from TTS import ttsPlay
from gptMessagePrepare import prepare_message


def play20Questions(inputType):
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
        iprompt,text,functionCalled=prepare_message(iprompt,inputType) #preparing the messages for ChatGPT
        print("Function called:", functionCalled)
        print("ChatGPT response:",text)

        if functionCalled == "stop":
            break
