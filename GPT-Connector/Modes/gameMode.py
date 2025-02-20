import random
import sys

sys.path.append('../')

from TTS import ttsPlay
from gptMessagePrepare import prepare_message

from toolkit.gameTools import selectGameTools, triviaTools
from toolkit.noTools import noTools


def read_file_and_tokenize(file_name):
    try:
        # Open the file in read mode
        with open(file_name, 'r') as file:
            # Read the content of the file
            file_content = file.read()
            # Split the content into words
            words = file_content.split()
            return words
    except FileNotFoundError:
        print("File not found!")


def gameMode(inputType, button=None):
    game = chooseGame(inputType, button)
    if game == "twentyQuestions":
        return play20Questions(inputType, button)
    if game == "superheroTrivia":
        # print("----playing super hero trivia----")
        return playSuperheroTrivia(inputType, button)
    if game == "geoTrivia":
        return playGeoTrivia(inputType, button)

    if game in ["story", "stop", "distress", "coping"]:
        return game


def chooseGame(inputType, button=None):
    message = "What game would you like to play? We can play 20 questions, Superhero Trivia or geography trivia."
    print("OWL response:", message)
    ttsPlay(message)
    iprompt = []
    assert1 = {"role": "system", "content": "You are an ai friend of a child"}
    assert2 = {"role": "assistant",
               "content": "You are attempting to find out whether a child wants to play 20 questions, Superhero Trivia or geography trivia."}
    iprompt.append(assert1)
    iprompt.append(assert2)
    game = None
    while game == None:
        _, _, game = prepare_message(iprompt, inputType, selectGameTools, button=button)

    return game


def playGeoTrivia(inputType, button=None):
    geoTopicList = read_file_and_tokenize("Modes/gameModeTopics.txt")

    iprompt = []
    assert1 = {"role": "system", "content": "You are an ai friend to a child"}
    randomGeoTopic = random.choice(geoTopicList)

    content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{randomGeoTopic}", and georgraphy topics. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""

    assert2 = {"role": "assistant", "content": content}

    iprompt.append(assert1)
    iprompt.append(assert2)
    iprompt.append({"role": "user", "content": "Please ask me a question and remember to only ask me questions!"})
    iprompt, text, functionCalled = prepare_message(iprompt, 2, noTools)
    while True:
        randomGeoTopic = random.choice(geoTopicList)

        content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{randomGeoTopic}", and georgraphy topics. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""

        assert2 = {"role": "assistant", "content": content}
        iprompt[1] = assert2

        iprompt, text, functionCalled = prepare_message(iprompt, inputType, triviaTools,
                                                        button=button)  # preparing the messages for ChatGPT

        if functionCalled in ["story", "stop", "distress", "coping"]:
            return functionCalled


def playSuperheroTrivia(inputType, button=None):
    listOfSuperheroes = ["Superman", "Spiderman", "Iron Man", "Wonder Woman", "Batman", "Aquaman", "Captain America",
                         "Incredible Hulk", "Thor", "Ant-Man", "Wolverine"]

    iprompt = []
    assert1 = {"role": "system", "content": "You are an ai friend to a child"}
    randomSuperhero = random.choice(listOfSuperheroes)

    content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{randomSuperhero}", superheroes and superhero movies. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""

    assert2 = {"role": "assistant", "content": content}

    iprompt.append(assert1)
    iprompt.append(assert2)
    iprompt.append({"role": "user", "content": "Please ask me a question and remember to only ask me questions!"})
    iprompt, text, functionCalled = prepare_message(iprompt, 2, noTools)
    while True:
        randomSuperhero = random.choice(listOfSuperheroes)

        content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{randomSuperhero}", superheroes and superhero movies. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""

        assert2 = {"role": "assistant", "content": content}
        iprompt[1] = assert2

        iprompt, text, functionCalled = prepare_message(iprompt, inputType, triviaTools,
                                                        button=button)  # preparing the messages for ChatGPT

        if functionCalled in ["story", "stop", "distress", "coping"]:
            return functionCalled


def play20Questions(inputType, button=None):
    secretObjectType = random.choice(["animal", "plant", "inanimate object", "historical person"])
    secretObjectLetter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    secretObjectQuestion = "Choose a random example of a " + secretObjectType + ". It should start with the letter: " + secretObjectLetter + ". Your response should be a single word and nothing else. Do not tell the use what the object is unless explicitly said so. Only respond yes or no."

    iprompt = []
    assert1 = {"role": "system", "content": "You are still waiting to decide what your secret object is."}
    assert2 = {"role": "assistant", "content": secretObjectQuestion}

    firstMessage = "Lets play 20 questions. I've thought of a word and you need to guess it."
    print("OWL response:", firstMessage)
    ttsPlay(firstMessage)

    iprompt.append(assert1)
    iprompt.append(assert2)

    while True:
        iprompt, text, functionCalled = prepare_message(iprompt, inputType, triviaTools,
                                                        button=button)  # preparing the messages for ChatGPT

        if functionCalled in ["story", "stop", "distress", "coping"]:
            return functionCalled
