print("Starting GPT-Connector...")
import ctypes
from ctypes import c_char_p, c_int, CFUNCTYPE


print("Loading ALSA library...")
try:
    _libasound = ctypes.cdll.LoadLibrary("libasound.so")
    ALSA_ERR_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
    def _alsa_err_handler(file, line, func, err, fmt):  # noqa: U100
        pass
    _alsa_silencer = ALSA_ERR_FUNC(_alsa_err_handler)
    _libasound.snd_lib_error_set_handler(_alsa_silencer)
except Exception as e:
    print("Error loading ALSA library:", e)

print("Loading JACK library...")
try:
    _libjack = ctypes.cdll.LoadLibrary("libjack.so.0")   # .so may vary
    JACK_ERR_FUNC = CFUNCTYPE(None, c_char_p)
    _jack_silencer = JACK_ERR_FUNC(lambda msg: None)
    _libjack.jack_set_error_function(_jack_silencer)
except Exception as e:
    print("Error loading JACK library:", e)



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
