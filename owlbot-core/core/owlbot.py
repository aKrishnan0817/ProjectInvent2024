from openai import Client
from modes.base import BaseMode, ModeError
from modes.distress import DistressMode
from modes.game import GameMode
from modes.psychoeducation import PsychoeducationMode
from modes.story import StoryMode
from modes.coping import CopingMode
from modes.stop import StopMode
from utils.tts import tts_play

class ModeManager:
    def __init__(self, owlbot_agent):
        self.owlbot_agent = owlbot_agent
        self.current_mode = None
        self.modes = {
            "distress": DistressMode(owlbot_agent),
            "game": GameMode(owlbot_agent),
            "psychoeducation": PsychoeducationMode(owlbot_agent),
            "story": StoryMode(owlbot_agent),
            "coping": CopingMode(owlbot_agent),
            "stop": StopMode(owlbot_agent)
        }
        
    def switch_mode(self, mode_name, *args, **kwargs):
        try:
            if mode_name not in self.modes:
                raise ModeError(f"Unknown mode: {mode_name}")
                
            # Handle mode transition
            if self.current_mode:
                self.current_mode.exit()
                
            new_mode = self.modes[mode_name]
            self.current_mode = new_mode
            result = new_mode.enter(*args, **kwargs)
            
            return result
            
        except Exception as e:
            # Log error and handle gracefully
            print(f"Error switching to mode {mode_name}: {e}")
            return None

    def get_current_mode(self):
        return self.current_mode

    def is_mode_active(self, mode_name):
        return mode_name in self.modes and self.modes[mode_name].is_active

class OwlbotAgent:
    def __init__(self, model, api_key, system_prompt=None):
        self.system_prompt = system_prompt
        self.model = model
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        self.api_key = api_key
        self.mode_manager = ModeManager(self)
        
        if "deepseek" in model:
            self.client = Client(api_key=api_key, base_url="https://api.deepseek.com")
        else:
            self.client = Client(api_key=api_key)

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt
        self.conversation_history[0] = {"role": "system", "content": system_prompt}

    def add_to_history(self, agent, input):
        if agent == "owlbot":
            self.conversation_history.append({"role": "assistant", "content": input})
        if agent == "child":
            self.conversation_history.append({"role": "user", "content": input})

    def prepare_message(self, iprompt, input_type, tools=None, button=None):
        """Prepare and process a message using the current mode's tools"""
        if self.mode_manager.current_mode:
            return self.mode_manager.current_mode.handle_input(
                iprompt=iprompt,
                input_type=input_type,
                button=button
            )
        return self.get_response(iprompt[-1]["content"] if iprompt else "")

    def get_response(self, user_input):
        bot_response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            max_tokens=150,
            temperature=0.7,
            presence_penalty=0.6,
        )
        bot_response = bot_response.choices[0].message.content
        self.add_to_history("child", user_input)
        self.add_to_history("owlbot", bot_response)
        return bot_response

    def clear_history(self):
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

    def get_history(self):
        return self.conversation_history

    def speak(self, message):
        """Speak a message using text-to-speech"""
        print("OWL response:", message)
        tts_play(message) 