class BaseMode:
    def __init__(self, owlbot_agent):
        self.owlbot_agent = owlbot_agent
        self.is_active = False
        
    def enter(self, *args, **kwargs):
        """Called when entering the mode"""
        self.is_active = True
        return self.handle_input(*args, **kwargs)
        
    def exit(self):
        """Called when exiting the mode"""
        self.is_active = False
        
    def handle_input(self, *args, **kwargs):
        """Handle input in this mode"""
        pass

    def speak(self, message):
        """Speak a message using the agent's TTS"""
        self.owlbot_agent.speak(message)

    def prepare_message(self, iprompt, input_type, button=None):
        """Prepare a message using the agent's functionality"""
        return self.owlbot_agent.prepare_message(iprompt, input_type, button=button)

    def get_response(self, user_input):
        """Get a response from the agent"""
        return self.owlbot_agent.get_response(user_input)

class ModeError(Exception):
    pass 