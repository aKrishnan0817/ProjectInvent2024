import random
import sys

sys.path.append('../')

from TTS import ttsPlay
from gptMessagePrepare import prepare_message


def psychoeducation(inputType, button):
    topic = chooseTopic(inputType, button)
    return pschychoeducationTopic(inputType, button, topic)

    if topic in ["story", "stop", "distress", "coping"]:
        return topic


def chooseTopic(inputType, button):
    message = "What is a psychoeducation topic you would like to learn: "
    print("OWL response:", message)
    ttsPlay(message)
    iprompt = []
    assert1 = {"role": "system", "content": "You are an ai friend of a child"}
    assert2 = {"role": "assistant",
               "content": "You are attempting to find out what psychoeducation module a child wants to learn"}
    iprompt.append(assert1)
    iprompt.append(assert2)
    topic = None
    while topic == None:
        _, _, topic = prepare_message(iprompt, inputType, selectGameTools, button=button)

    return topic


def psychoeducationTopic(inputType, button=None, topic):
    geoTopicList = read_file_and_tokenize("Modes/gameModeTopics.txt")

    iprompt = []
    assert1 = {"role": "system", "content": "You are an ai friend to a child"}
    randomGeoTopic = random.choice(geoTopicList)

    content = f"""You are now a psychoeducation teacher. Your job is to teach a child information about "{topic}". When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""

    assert2 = {"role": "assistant", "content": content}
