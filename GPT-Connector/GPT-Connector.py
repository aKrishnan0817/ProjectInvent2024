from Modes.gameMode import gameMode
from Modes.storyMode import storyMode
from Modes.distress import distressMode
from Modes.copingSkillsMode import copingSkills

from gptMessagePrepare import prepare_message

import sensitiveData
from piComponents import piComponents


iprompt = []
assert1={"role": "system", "content": "You are a frined of a nine year old boy"}
assert2={"role": "assistant", "content": "You are to act and talk the way a younger child would to his friends"}
iprompt.append(assert1)
iprompt.append(assert2)

#1 for typing 0 for speaking
inputType = 0

#-----CONFIG FOR DISTRESS MODE------
email = sensitiveData.emailAddress
password = sensitiveData.emailPassword
gaurdianEmail = sensitiveData.userContactAddress #put this in sensitiveData as to not expose anyones private number
#---------------------------------------------
mainFuncCall = None
functionCalled = None

button = piComponents(buttonPin=2,ledPin=4)

while(True):

    if mainFuncCall == functionCalled:
        iprompt,text,functionCalled=prepare_message(iprompt,inputType,button=button) #preparing the messages for ChatGPT

    mainFuncCall = functionCalled


    if functionCalled == "distress":
        functionCalled = distressMode(email,password,gaurdianEmail,iprompt,inputType,button=button)

    if functionCalled == "game":
        functionCalled=gameMode(inputType,button=button)

    if functionCalled == "story":
        functionCalled= storyMode(inputType,button)

    if functionCalled == "coping":
        functionCalled= copingSkills(inputType,iprompt,button=button)

    if functionCalled == "stop":
        iprompt,text,functionCalled=prepare_message(iprompt,2,button=button)
