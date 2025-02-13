
from openai import OpenAI
import random
import sys

sys.path.append('../')

from TTS import ttsPlay
from gptMessagePrepare import prepare_message

from toolkit.noTools import noTools
from toolkit.tools import tools


def psychoeducation(inputType, button):
    topic = chooseTopic(inputType,button)
    if topic == "twentyQuestions":
        return play20Questions(inputType,button)
    if topic =="superheroTrivia":
        #print("----playing super hero trivia----")
        return playSuperheroTrivia(inputType,button)
    if topic == "geoTrivia":
        return playGeoTrivia(inputType,button)

    if topic in ["story","stop","distress","coping"]:
        return topic
    

def chooseTopic(inputType, button):
    message = "What is a psychoeducation topic you would like to learn: "
    print("OWL response:",message)
    ttsPlay(message)
    iprompt = []
    assert1={"role": "system", "content": "You are an ai friend of a child"}
    assert2={"role": "assistant", "content": "You are attempting to find out what psychoeducation module a child wants to learn"}
    iprompt.append(assert1)
    iprompt.append(assert2)
    topic = None
    while topic == None:
        _,_,topic = prepare_message(iprompt, inputType , selectGameTools,button=button)

    return topic
    
