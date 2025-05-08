from modes.base import BaseMode
import threading
import pygame
from tools.story_tools import select_story_tools, story_type_select
from tools.no_tools import no_tools
from utils.tts import tts_play

class StoryMode(BaseMode):
    def __init__(self, owlbot_agent):
        super().__init__(owlbot_agent)
        pygame.init()

    def handle_input(self, input_type, button=None):
        story_type = self._choose_story_type(input_type, button)
        if story_type in ["game", "stop", "distress", "coping"]:
            return story_type

        if story_type == "randomStory":
            return self._generate_random_story(input_type, button)
        elif story_type == "defaultStory":
            return self._play_default_story(input_type, button)

    def _choose_story_type(self, input_type, button):
        first_message = "Would you like to listen to a story from my large collection? Or I can create a story based on a few random words you give me!"
        print("OWL response:", first_message)
        tts_play(first_message)
        
        iprompt = [
            {"role": "system", "content": "You are an audio book app"},
            {"role": "assistant", "content": "You are attempting to find out whether the user would like a story randomly generated or an existing story"}
        ]
        
        story_type = None
        while story_type is None:
            iprompt, _, story_type = prepare_message(iprompt, input_type, story_type_select, button=button)
        return story_type

    def _choose_story(self, input_type, button):
        message = "What is the name or type of story you'd like to listen to?"
        print("OWL response:", message)
        tts_play(message)
        
        iprompt = [
            {"role": "system", "content": "You are an audio book app"},
            {"role": "assistant", "content": "You are attempting to find out what story the user would like to listen to based on the name and description"}
        ]
        
        story_name = None
        while story_name is None:
            _, _, story_name = prepare_message(iprompt, input_type, select_story_tools, button=button)
        return story_name

    def _generate_random_story(self, input_type, button):
        # Implementation for generating random stories
        pass

    def _play_default_story(self, input_type, button):
        story_name = self._choose_story(input_type, button)
        if story_name in ["game", "stop", "distress", "coping"]:
            return story_name
            
        audio_file = f"modes/story_mode_audios/{story_name}.mp3"
        self._play_audio(audio_file, button)
        return None

    def _play_audio(self, audio_file, button):
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        if button and button.get_button_use():
            stop_thread = threading.Thread(target=self._listen_for_stop, args=(button,))
            stop_thread.start()
            stop_thread.join()
        else:
            while pygame.mixer.music.get_busy():
                continue

    def _listen_for_stop(self, button):
        button.check_button_press()
        pygame.mixer.music.stop()
        pygame.quit() 