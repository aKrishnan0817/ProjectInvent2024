
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
    if game =="superheroTrivia":
        #print("----playing super hero trivia----")
        return playSuperheroTrivia(inputType)
    if game == "geoTrivia":
        return playGeoTrivia(inputType)

    if game in ["story","stop","distress","coping"]:
        return game

def chooseGame(inputType):
    message = "What game would you like to play? We can play 20 questions, Superhero Trivia or geography trivia."
    print("ChatGPT response:",message)
    ttsPlay(message)
    iprompt = []
    assert1={"role": "system", "content": "You are an ai friend of a child"}
    assert2={"role": "assistant", "content": "You are attempting to find out whether a child wants to play 20 questions, Superhero Trivia or geography trivia."}
    iprompt.append(assert1)
    iprompt.append(assert2)
    game = None
    while game == None:
        _,_,game = prepare_message(iprompt, inputType , selectGameTools)

    return game

def playGeoTrivia(inputType):
    iprompt = []
    assert1={"role": "system", "content": "You are an ai friend to a child"}
    assert2={"role": "assistant", "content": "You are to play geography trivia with a 9 year old child so don't make the question too hard."}

    firstMessage = "Lets do some geography trivia! Try to answer all the questions as well as you can!"
    print(firstMessage)
    ttsPlay(firstMessage)

    iprompt.append(assert1)
    iprompt.append(assert2)

    while True:
        iprompt,text,functionCalled=prepare_message(iprompt,inputType,triviaTools) #preparing the messages for ChatGPT

        if functionCalled in ["story","stop","distress","coping"]:
            return functionCalled
def playSuperheroTrivia(inputType):
    listOfSuperheroes = ["Superman", "Spiderman", "Iron Man", "Wonder Woman","Batman","Aquaman","Captain America","Incredible Hulk","Thor","Ant-Man","Wolverine"]

    iprompt = []
    assert1={"role": "system", "content": "You are an ai friend to a child"}
    randomSuperhero = random.choice(listOfSuperheroes)

    content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{randomSuperhero}", superheroes and superhero movies. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""

    assert2={"role": "assistant", "content": content}

    iprompt.append(assert1)
    iprompt.append(assert2)
    iprompt.append({"role": "user", "content": "Please ask me a question and remember to only ask me questions!"})
    iprompt,text,functionCalled=prepare_message(iprompt,2,noTools)
    while True:
        randomSuperhero = random.choice(listOfSuperheroes)

        content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{randomSuperhero}", superheroes and superhero movies. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""

        assert2={"role": "assistant", "content": content}
        iprompt[1] = assert2

        iprompt,text,functionCalled=prepare_message(iprompt,inputType,triviaTools) #preparing the messages for ChatGPT

        if functionCalled in ["story","stop","distress","coping"]:
            return functionCalled

def play20Questions(inputType):
    secretObjectType = random.choice(["animal", "plant", "inanimate object", "historical person"])
    secretObjectLetter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    secretObjectQuestion = "Choose a random example of a " + secretObjectType + ". It should start with the letter: " + secretObjectLetter + ". Your response should be a single word and nothing else. Do not tell the use what the object is unless explicitly said so. Only respond yes or no."

    iprompt = []
    assert1={"role": "system", "content": "You are still waiting to decide what your secret object is."}
    assert2={"role": "assistant", "content": secretObjectQuestion}

    firstMessage = "Lets play 20 questions. I've thought of a word and you need to guess it."
    print("ChatGPT response:",firstMessage)
    ttsPlay(firstMessage)

    iprompt.append(assert1)
    iprompt.append(assert2)

    while True:
        iprompt,text,functionCalled=prepare_message(iprompt,inputType,triviaTools) #preparing the messages for ChatGPT

        if functionCalled in ["story","stop","distress","coping"]:
            return functionCalled
