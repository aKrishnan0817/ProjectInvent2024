from modes.base import BaseMode
import threading
import time
from utils.email import send_email, check_inbox, check_text_confirmation
from tools.distress_tools import distress_conversation_tools
from tools.no_tools import no_tools

class DistressMode(BaseMode):
    def __init__(self, owlbot_agent):
        super().__init__(owlbot_agent)
        self.func_called = None
        self.conf_received = False

    def handle_input(self, email, password, guardian_email, iprompt, input_type, button=None):
        # Send distress notification
        message = "Hi Hope, this is a notification that Jonah may be in a distressed state right now. Please check in on him as soon as you can."
        subject = 'AI Companion: Notification for Jonah'
        send_email(email, password, guardian_email, subject, message)

        # Start conversation and email check threads
        conversation_thread = threading.Thread(
            target=self._distress_conversation,
            args=(iprompt, input_type, button)
        )
        refresh_check_thread = threading.Thread(
            target=self._refresh_check,
            args=(email, password, guardian_email)
        )

        conversation_thread.start()
        refresh_check_thread.start()

        conversation_thread.join()
        refresh_check_thread.join()

        return self.func_called

    def _distress_conversation(self, iprompt, input_type, button):
        assert1 = {"role": "system", "content": "You are talking to a child in distress."}
        assert2 = {"role": "assistant",
                  "content": "You are talking to a child in distress. Logically address any concerns that he has and be conservative when making decisions."}
        iprompt[0] = assert1
        iprompt[1] = assert2
        iprompt.append(iprompt[len(iprompt) - 1])
        
        iprompt, _, _ = self.prepare_message(iprompt, 2, button=button)
        
        while True:
            iprompt, text, function_called = self.prepare_message(
                iprompt, input_type, button=button
            )

            if function_called in ["story", "stop", "game", "coping"]:
                self.func_called = function_called
                break

    def _refresh_check(self, email, password, guardian_email):
        while True and self.func_called is None:
            text = check_inbox(email, password, guardian_email)
            if text is not None:
                if check_text_confirmation(text):
                    print("Received Confirmation")
                    self.conf_received = True
                    break
            time.sleep(5) 