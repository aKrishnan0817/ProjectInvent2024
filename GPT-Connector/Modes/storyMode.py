import pygame
import threading
import sys

sys.path.append('../')

from toolkit.storyTools import selectStoryTools, storyTypeSelect
from toolkit.noTools import noTools


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



def listen_for_stop():

    input("Press Enter to stop the audio\n")  # This will block until Enter key is pressed
    pygame.mixer.music.stop()
    pygame.quit()

def chooseStory(inputType):
    message = "What is the name or type of story you'd like to listen to?"
    print(message)
    ttsPlay(message)
    iprompt = []
    assert1={"role": "system", "content": "You are an audio book app"}
    assert2={"role": "assistant", "content": "You are attempting to find out what story the user would like to listen to based on the name and description"}
    storyName = None
    while storyName == None:
        _,_,storyName = prepare_message(iprompt, inputType , selectStoryTools)

    #the function called should be the name of the story
    return storyName


#if the user wants a randomly generated story or pre recorded
def chooseStoryType(inputType):
    firstMessage = "Would you like to listen to a story from my large collection? Or I can create a story based on a few random words you give me!"
    print(firstMessage)
    ttsPlay(firstMessage)
    iprompt = []
    assert1={"role": "system", "content": "You are an audio book app"}
    assert2={"role": "assistant", "content": "You are attempting to find out whether the user would like a story randomly generated or an existing story"}
    storyType = None
    while storyType == None:
        iprompt,_,storyType = prepare_message(iprompt, inputType , storyTypeSelect)
    return storyType

def generateRandomStory(inputType):
    message = "Could you give me a few words that I can use to make the story?"
    print(message)
    #ttsPlay(message)

    if inputType:
        print("Type your words and press enter:")
        words = input("")
        print(words)
    else:
        words = speech_to_text()



    iprompt = []
    assert1={"role": "system", "content": "You are an audio book app"}
    assert2={"role": "assistant", "content": "You  MUST generate a short story appropaite for a 9 year old based on these random words: "+ words}
    iprompt.append({"role": "user", "content": "Please tell me a short story based on the words I specified  : " + words})
    text = None
    _,text,storyType = prepare_message(iprompt, 2 ,noTools )
    while text == None:
        message = "I apologize the request didn't work. Could you give me another set of words?"
        print(message)
        #ttsPlay(message)
        if inputType:
            print("Type your words and press enter:")
            words = input("")
            print(words)
        else:
            words = speech_to_text()
        _,text,storyType = prepare_message(iprompt, 2 , noTools )


def storyMode(inputType):
    storyType = chooseStoryType(inputType)



    if storyType == "randomStory":
        print("----random story called----")
        randomStory_thread = threading.Thread(target=generateRandomStory, args=(inputType,))
        randomStory_thread.start()
        randomStory_thread.join()
    if storyType == "defaultStory":
        storyName = chooseStory(inputType)
        audio_file = "Modes/storyModeAudios/"+storyName+".mp3"
        play_thread = threading.Thread(target=play_audio, args=(audio_file,))
        play_thread.start()
        play_thread.join()



    #stop_thread = threading.Thread(target=listen_for_stop)
    #stop_thread.start()
    #stop_thread.join()



if __name__ == "__main__":
    generateRandomStory(1)
