print("Starting GPT-Connector...")
print("Destroying ALSA error handler...")
from ctypes import c_char_p, c_int, CFUNCTYPE, cdll

# STEP 1: build a C callback that does nothing
ERROR_HANDLER_FUNC = CFUNCTYPE(None,     # return type
                               c_char_p, # file
                               c_int,    # line
                               c_char_p, # function
                               c_int,    # err
                               c_char_p) # fmt
def _py_alsa_err_handler(file, line, func, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(_py_alsa_err_handler)

# STEP 2: load libasound and register the handler
asound = cdll.LoadLibrary("libasound.so")
asound.snd_lib_error_set_handler(c_error_handler)




import sensitiveData
from Modes.copingSkillsMode import copingSkills
from Modes.distress import distressMode
from Modes.gameMode import gameMode
from Modes.storyMode import storyMode
from Modes.emotionTracking import *
from gptMessagePrepare import prepare_message
from piComponents import piComponents

iprompt = []
assert1 = {"role": "system", "content": "You are a frined of a nine year old boy"}
assert2 = {"role": "assistant", "content": "You are to act and talk the way a younger child would to his friends"}
iprompt.append(assert1)
iprompt.append(assert2)

# 1 for typing 0 for speaking
inputType = 0

# -----CONFIG FOR DISTRESS MODE------
email = sensitiveData.emailAddress
password = sensitiveData.emailPassword
gaurdianEmail = sensitiveData.userContactAddress  # put this in sensitiveData as to not expose anyones private number
# ---------------------------------------------
mainFuncCall = None
functionCalled = "record_emotion_intensity"

button = piComponents(buttonPin=2, ledPin=4)

while (True):

    if mainFuncCall == functionCalled:
        iprompt, text, functionCalled = prepare_message(iprompt, inputType,
                                                        button=button)  # preparing the messages for ChatGPT

    mainFuncCall = functionCalled
    if functionCalled == "record_emotion_intensity":
        functionCalled = emotionTracking(inputType, button = button)

    if functionCalled == "distress":
        functionCalled = distressMode(email, password, gaurdianEmail, iprompt, inputType, button=button)

    if functionCalled == "game":
        functionCalled = gameMode(inputType, button=button)

    if functionCalled == "story":
        functionCalled = storyMode(inputType, button)

    if functionCalled == "coping":
        functionCalled = copingSkills(inputType, iprompt, button=button)

    if functionCalled == "stop":
        iprompt, text, functionCalled = prepare_message(iprompt, 2, button=button)
