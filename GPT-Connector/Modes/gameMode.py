
from openai import OpenAI
import random
import sys

sys.path.append('../')

from TTS import ttsPlay
from gptMessagePrepare import prepare_message

from toolkit.gameTools import selectGameTools, triviaTools
from toolkit.noTools import noTools


def gameMode(inputType):
    game = chooseGame(inputType)
    if game == "twentyQuestions":
        return play20Questions(inputType)
    if game =="movieTrivia":
        return playMovieTrivia(inputType)
    if game == "geoTrivia":
        return playGeoTrivia(inputType)

    if game in ["story","stop","distress","coping"]:
        return game

def chooseGame(inputType):
    message = "What game would you like to play? We can play 20 questions, movie Trivia or geography trivia."
    print(message)
    ttsPlay(message)
    iprompt = []
    assert1={"role": "system", "content": "You are an ai friend of a child"}
    assert2={"role": "assistant", "content": "You are attempting to find out whether a child wants to play 20 questions, movie Trivia or geogrpahy trivia."}
    iprompt.append(assert1)
    iprompt.append(assert2)
    game = None
    while game == None:
        _,_,game = prepare_message(iprompt, inputType , selectGameTools)

    return game

def playGeoTrivia(inputType):
    iprompt = []
    assert1={"role": "system", "content": "You are an ai friend to a child"}
    assert2={"role": "assistant", "content": "You are to play geogrpahy trivia with a 9 year old child so dont make the question too hard."}

    firstMessage = "Lets do some georgaphy trivia! Try to answer all the questions as well as you can!"
    print(firstMessage)
    ttsPlay(firstMessage)

    iprompt.append(assert1)
    iprompt.append(assert2)

    while True:
        iprompt,text,functionCalled=prepare_message(iprompt,inputType,triviaTools) #preparing the messages for ChatGPT
        print("Function called:", functionCalled)
        print("ChatGPT response:",text)

        if functionCalled in ["story","stop","distress","coping"]:
            return functionCalled
def playMovieTrivia(inputType):
    iprompt = []
    assert1={"role": "system", "content": "You are an ai friend to a child"}
    assert2={"role": "assistant", "content": "You are to play movie trivia with a 9 year old child so dont make the question too hard. You are the only one to ask questions and when they respond they are only responding to the question you have asked."}

    firstMessage = "Lets do some movie trivia! Try to answer all the questions as well as you can!"
    print(firstMessage)
    ttsPlay(firstMessage)

    iprompt.append(assert1)
    iprompt.append(assert2)

    while True:
        iprompt,text,functionCalled=prepare_message(iprompt,inputType,triviaTools) #preparing the messages for ChatGPT
        print("Function called:", functionCalled)
        print("ChatGPT response:",text)

        print("functionCalled")
        if functionCalled in ["story","stop","distress","coping"]:
            return functionCalled

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
        iprompt,text,functionCalled=prepare_message(iprompt,inputType,triviaTools) #preparing the messages for ChatGPT
        print("Function called:", functionCalled)
        print("ChatGPT response:",text)

        if functionCalled in ["story","stop","distress","coping"]:
            return functionCalled
