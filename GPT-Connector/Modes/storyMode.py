import sys
import threading

import pygame

sys.path.append('../')

from toolkit.storyTools import selectStoryTools, storyTypeSelect
from toolkit.noTools import noTools
from speech_to_text import speech_to_text

from gptMessagePrepare import prepare_message
from TTS import ttsPlay


def play_audio(audio_file):
    # Initialize pygame
    pygame.init()
    # Load the audio file
    pygame.mixer.music.load(audio_file)
    # Play the audio file
    pygame.mixer.music.play()
    # Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        continue

    print("--finished")


def listen_for_stop(button):
    button.checkButtonPress()  # This will block until button is pressed
    pygame.mixer.music.stop()
    pygame.quit()


def chooseStory(inputType, button):
    message = "What is the name or type of story you'd like to listen to?"
    print("OWL response:", message)
    ttsPlay(message)
    iprompt = []
    assert1 = {"role": "system", "content": "You are an audio book app"}
    assert2 = {"role": "assistant",
               "content": "You are attempting to find out what story the user would like to listen to based on the name and description"}
    iprompt.append(assert1)
    iprompt.append(assert2)
    storyName = None
    while storyName == None:
        _, _, storyName = prepare_message(iprompt, inputType, selectStoryTools, button=button)
        print(storyName)
    # the function called should be the name of the story
    return storyName


# if the user wants a randomly generated story or pre recorded
def chooseStoryType(inputType, button):
    firstMessage = "Would you like to listen to a story from my large collection? Or I can create a story based on a few random words you give me!"
    print("OWL response:", firstMessage)
    ttsPlay(firstMessage)
    iprompt = []
    assert1 = {"role": "system", "content": "You are an audio book app"}
    assert2 = {"role": "assistant",
               "content": "You are attempting to find out whether the user would like a story randomly generated or an existing story"}
    iprompt.append(assert1)
    iprompt.append(assert2)
    storyType = None
    while storyType == None:
        iprompt, _, storyType = prepare_message(iprompt, inputType, storyTypeSelect, button=button)
        print(storyType)
    return storyType


def generateRandomStory(inputType, button):
    message = "Could you give me a few words that I can use to make the story?"
    print("OWL response:", message)
    ttsPlay(message)

    if inputType:
        print("Type your words and press enter:")
        words = input("")
    else:
        words = speech_to_text(button)

    iprompt = []
    assert1 = {"role": "system", "content": "You are an audio book app"}
    assert2 = {"role": "assistant", "content": "You  MUST generate a short story appropriate for a 9 year old based on "
                                               "these random words: " + words}
    iprompt.append(
        {"role": "user", "content": "Please tell me a short story based on the words I specified  : " + words})
    iprompt.append(assert1)
    iprompt.append(assert2)
    text = None
    _, text, storyType = prepare_message(iprompt, 2, noTools)
    while text == None:
        message = "I apologize the request didn't work. Could you give me another set of words?"
        print("ChatGPT response:", message)
        # ttsPlay(message)
        if inputType:
            print("Type your words and press enter:")
            words = input("")
        else:
            words = speech_to_text()
        _, text, storyType = prepare_message(iprompt, 2, noTools, button=button)


def storyMode(inputType, button):
    storyType = chooseStoryType(inputType, button)
    print(storyType)
    if storyType in ["game", "stop", "distress", "coping"]:
        return storyType

    if storyType == "randomStory":
        randomStory_thread = threading.Thread(target=generateRandomStory, args=(inputType, button))
        randomStory_thread.start()
        randomStory_thread.join()
    if storyType == "defaultStory":
        storyName = chooseStory(inputType, button)
        if storyName in ["game", "stop", "distress", "coping"]:
            return storyName
        audio_file = "Modes/storyModeAudios/" + storyName + ".mp3"
        play_audio(audio_file)
        """play_thread = threading.Thread(target=play_audio, args=(audio_file))
        play_thread.start()
        play_thread.join()

    if button.getButtonUse:
        stop_thread = threading.Thread(target=listen_for_stop, args=(button))
        stop_thread.start()
        stop_thread.join()"""

    return None


if __name__ == "__main__":
    generateRandomStory(1)
