from modes.base import BaseMode
from utils.message_prepare import prepare_message
from tools.no_tools import no_tools

class StopMode(BaseMode):
    def handle_input(self, iprompt, input_type, button=None):
        return prepare_message(iprompt, input_type, no_tools, button=button) 