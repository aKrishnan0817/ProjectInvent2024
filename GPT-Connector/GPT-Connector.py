from Modes.gameMode import gameMode
from Modes.storyMode import storyMode
from Modes.distress import distressMode
from Modes.copingSkillsMode import copingSkills

from gptMessagePrepare import prepare_message

import sensitiveData

iprompt = []
assert1={"role": "system", "content": "You are a frined of a nine year old boy"}
assert2={"role": "assistant", "content": "You are to act and talk the way a younger child would to his friends"}
iprompt.append(assert1)
iprompt.append(assert2)

#1 for typing 0 for speaking
inputType = 1

#-----CONFIG FOR DISTRESS MODE------
email = sensitiveData.emailAddress
password = sensitiveData.emailPassword
gaurdianEmail = sensitiveData.userContactAddress #put this in sensitiveData as to not expose anyones private number
#---------------------------------------------
mainFuncCall = None
functionCalled = None
while(True):

    if mainFuncCall == functionCalled:
        iprompt,text,functionCalled=prepare_message(iprompt,inputType) #preparing the messages for ChatGPT

    mainFuncCall = functionCalled


    if functionCalled == "distress":
        functionCalled = distressMode(email,password,gaurdianEmail,iprompt,inputType)

    if functionCalled == "game":
        functionCalled=gameMode(inputType)

    if functionCalled == "story":
        functionCalled= storyMode(inputType)

    if functionCalled == "coping":
        functionCalled= copingSkills(inputType,iprompt)
