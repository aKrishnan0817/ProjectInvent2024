from modes.base import BaseMode
from tools.psychoeducation_tools import psychoeducation_tools
from tools.no_tools import no_tools
from utils.tts import tts_play

class PsychoeducationMode(BaseMode):
    def __init__(self, owlbot_agent):
        super().__init__(owlbot_agent)
        self.topics = {
            "anxiety": self._anxiety_topic,
            "emotions": self._emotions_topic,
            "coping": self._coping_topic,
            "thoughts": self._thoughts_topic
        }

    def handle_input(self, input_type, iprompt, button=None):
        topic = self._choose_topic(input_type, button)
        if topic in self.topics:
            return self.topics[topic](input_type, iprompt, button)
        return topic  # Return the mode name if it's a mode switch

    def _choose_topic(self, input_type, button):
        message = "What psychoeducation topic would you like to learn about? We can talk about anxiety, emotions, coping skills, or thoughts."
        print("OWL response:", message)
        tts_play(message)
        
        iprompt = [
            {"role": "system", "content": "You are an ai friend of a child"},
            {"role": "assistant", "content": "You are attempting to find out what psychoeducation topic a child wants to learn"}
        ]
        
        topic = None
        while topic is None:
            _, _, topic = prepare_message(iprompt, input_type, no_tools, button=button)
        return topic

    def _anxiety_topic(self, input_type, iprompt, button):
        system_prompt = """
        Your job is to teach a child about anxiety in an age-appropriate way.
        Your responses should be brief, engaging, and accurate.
        Discuss one concept at a time and check their understanding.
        If they change the subject, gently direct them back to the topic.
        """
        
        if iprompt and len(iprompt) > 0:
            if iprompt[0]["role"] == "system":
                iprompt[0]["content"] = system_prompt
            else:
                iprompt.insert(0, {"role": "system", "content": system_prompt})
        else:
            iprompt = [{"role": "system", "content": system_prompt}]

        while True:
            iprompt, text, function_called = prepare_message(iprompt, input_type, psychoeducation_tools, button=button)
            if function_called in ["story", "stop", "game", "coping"]:
                return function_called

    def _emotions_topic(self, input_type, iprompt, button):
        system_prompt = """
        Your job is to teach a child about emotions in an age-appropriate way.
        Help them understand different emotions, how to recognize them, and how to express them healthily.
        Use simple language and examples they can relate to.
        """
        
        if iprompt and len(iprompt) > 0:
            if iprompt[0]["role"] == "system":
                iprompt[0]["content"] = system_prompt
            else:
                iprompt.insert(0, {"role": "system", "content": system_prompt})
        else:
            iprompt = [{"role": "system", "content": system_prompt}]

        while True:
            iprompt, text, function_called = prepare_message(iprompt, input_type, psychoeducation_tools, button=button)
            if function_called in ["story", "stop", "game", "coping"]:
                return function_called

    def _coping_topic(self, input_type, iprompt, button):
        system_prompt = """
        Your job is to teach a child about coping skills in an age-appropriate way.
        Focus on practical, easy-to-use techniques they can try right away.
        Make it fun and engaging, using examples they can relate to.
        """
        
        if iprompt and len(iprompt) > 0:
            if iprompt[0]["role"] == "system":
                iprompt[0]["content"] = system_prompt
            else:
                iprompt.insert(0, {"role": "system", "content": system_prompt})
        else:
            iprompt = [{"role": "system", "content": system_prompt}]

        while True:
            iprompt, text, function_called = prepare_message(iprompt, input_type, psychoeducation_tools, button=button)
            if function_called in ["story", "stop", "game", "coping"]:
                return function_called

    def _thoughts_topic(self, input_type, iprompt, button):
        system_prompt = """
        Your job is to teach a child about thoughts and thinking patterns in an age-appropriate way.
        Help them understand how thoughts affect feelings and behaviors.
        Use simple examples and encourage them to share their own experiences.
        """
        
        if iprompt and len(iprompt) > 0:
            if iprompt[0]["role"] == "system":
                iprompt[0]["content"] = system_prompt
            else:
                iprompt.insert(0, {"role": "system", "content": system_prompt})
        else:
            iprompt = [{"role": "system", "content": system_prompt}]

        while True:
            iprompt, text, function_called = prepare_message(iprompt, input_type, psychoeducation_tools, button=button)
            if function_called in ["story", "stop", "game", "coping"]:
                return function_called 