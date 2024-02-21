
from openai import OpenAI
import random
import sys

sys.path.append('../')

from TTS import ttsPlay
from gptMessagePrepare import prepare_message

from toolkit.noTools import noTools

def playGeoTrivia(inputType):
    iprompt = []
    assert1={"role": "system", "content": "You are an ai friend to a child"}
    assert2={"role": "assistant", "content": "Generate unique geogrpahy trivia questions. You are to play geogrpahy trivia with a 9 year old child so dont make the question too hard. You are the only one to ask questions. Once one quesitons is answered provided another question. Eachtime provide a completly seperate and unique questions not based off previosius responses."}

    firstMessage = "Lets do some georgaphy trivia! Try to answer all the questions as well as you can!"
    print(firstMessage)
    #ttsPlay(firstMessage)

    iprompt.append(assert1)
    iprompt.append(assert2)
    iprompt.append({"role": "user", "content": "Please ask me a question and remeber to only ask me questions!"})
    iprompt,text,functionCalled=prepare_message(iprompt,2,noTools)
    while True:
        iprompt,text,functionCalled=prepare_message(iprompt,inputType,noTools) #preparing the messages for ChatGPT
        #print("Function called:", functionCalled)
        #print("ChatGPT response:",text)

        if functionCalled == "stop":
            break

if __name__ == "__main__":
    playGeoTrivia(1)
