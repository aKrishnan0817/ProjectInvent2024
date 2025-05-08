from modes.base import BaseMode
from tools.coping_tools import coping_tools
from utils.tts import tts_play

class CopingMode(BaseMode):
    def __init__(self, owlbot_agent):
        super().__init__(owlbot_agent)
        self.coping_skills = {
            "relaxation": self._relaxation_script,
            "breathing": self._breathing_exercise,
            "grounding": self._grounding_exercise,
            "positive_thoughts": self._positive_thoughts
        }

    def handle_input(self, input_type, iprompt, button=None):
        skill = self._choose_skill(input_type, button)
        if skill in self.coping_skills:
            return self.coping_skills[skill](input_type, iprompt, button)
        return skill  # Return the mode name if it's a mode switch

    def _choose_skill(self, input_type, button):
        message = "What coping skill would you like to try? We can do relaxation exercises, breathing exercises, grounding techniques, or work on positive thoughts."
        print("OWL response:", message)
        tts_play(message)
        
        iprompt = [
            {"role": "system", "content": "You are an ai friend of a child"},
            {"role": "assistant", "content": "You are attempting to find out what coping skill a child wants to try"}
        ]
        
        skill = None
        while skill is None:
            _, _, skill = self.prepare_message(iprompt, input_type, coping_tools, button=button)
        return skill

    def _relaxation_script(self, input_type, iprompt, button):
        script = """
        I'm going to ask you to relax. In a few minutes, I am going to say some things that I hope will help you create a picture in your mind...
        I am also going to ask you to relax different parts of your body. Learning to relax will help you cope with angry, sad, and scary feelings.
        Find a comfortable position in your chair, not touching anyone, and take in a few relaxing breaths...
        Close your eyes and relax... Wiggle a little bit and make yourself comfortable...
        Alright, take a few relaxing breaths... breathe in... and breathe out... breath in... and breath out.
        That's it -- you are feeling peaceful. If you were angry, you can picture yourself moving from hot to cold on the thermometer.
        Becoming more and more relaxed, cold, peaceful.
        Now, with your eyes closed, pretend you are on a white fluffy cloud, high in the sky on a beautiful day.
        You are floating peacefully on that white fluffy cloud... moving very slowly... you are as light as a feather...
        and the fluffy cloud holds you safely... floating across the sky.
        Now, as I count from 1 to 3, imagine that you are sinking deeper and deeper into that cloud...so the cloud is all around you.
        1... 2... 3. You are enjoying the ride on the cloud.
        Now, notice on your toes and feet, how relaxed they feel... notice your legs...all the muscles on your legs are light and relaxed on the cloud...
        notice your arms... Notice your necks... notice your head... now you are totally relaxed... floating on the fluffy cloud...
        Remember that you can return to your very own cloud whenever you feel like you need to calm down and relax...
        Whenever you need to cool off... move from hot to cool on the thermometer...
        Now, we are getting ready to stop our ride on the cloud. We will stop on the count of three...1...2...3...
        Open your eyes and stretch a little..... How was that?
        """
        
        print("OWL response:", script)
        tts_play(script)
        
        iprompt = [
            {"role": "system", "content": "You are helping a child with relaxation techniques"},
            {"role": "assistant", "content": script},
            {"role": "user", "content": "How was that?"}
        ]
        
        while True:
            iprompt, text, function_called = self.prepare_message(iprompt, input_type, coping_tools, button=button)
            if function_called in ["story", "stop", "game", "distress"]:
                return function_called

    def _breathing_exercise(self, input_type, iprompt, button):
        exercise = """
        Let's try a simple breathing exercise. It's called the 4-7-8 breathing technique.
        First, find a comfortable position. You can sit or lie down.
        Now, let's begin:
        1. Breathe in through your nose for 4 seconds
        2. Hold your breath for 7 seconds
        3. Breathe out through your mouth for 8 seconds
        Let's try it together. I'll count for you...
        Ready? Here we go:
        Breathe in... 2... 3... 4...
        Hold... 2... 3... 4... 5... 6... 7...
        Breathe out... 2... 3... 4... 5... 6... 7... 8...
        Great job! Let's do that two more times...
        """
        
        print("OWL response:", exercise)
        tts_play(exercise)
        
        iprompt = [
            {"role": "system", "content": "You are helping a child with breathing exercises"},
            {"role": "assistant", "content": exercise},
            {"role": "user", "content": "How did that feel?"}
        ]
        
        while True:
            iprompt, text, function_called = self.prepare_message(iprompt, input_type, coping_tools, button=button)
            if function_called in ["story", "stop", "game", "distress"]:
                return function_called

    def _grounding_exercise(self, input_type, iprompt, button):
        exercise = """
        Let's try a grounding exercise called 5-4-3-2-1.
        This helps us focus on the present moment when we're feeling overwhelmed.
        I'll guide you through noticing things around you:
        1. Name 5 things you can see
        2. Name 4 things you can touch
        3. Name 3 things you can hear
        4. Name 2 things you can smell
        5. Name 1 thing you can taste
        Ready? Let's start with what you can see...
        """
        
        print("OWL response:", exercise)
        tts_play(exercise)
        
        iprompt = [
            {"role": "system", "content": "You are helping a child with grounding techniques"},
            {"role": "assistant", "content": exercise},
            {"role": "user", "content": "What do you see around you?"}
        ]
        
        while True:
            iprompt, text, function_called = self.prepare_message(iprompt, input_type, coping_tools, button=button)
            if function_called in ["story", "stop", "game", "distress"]:
                return function_called

    def _positive_thoughts(self, input_type, iprompt, button):
        exercise = """
        Let's work on positive thoughts. Sometimes when we're feeling down, it helps to think about good things.
        I'll help you think of positive things in different categories:
        1. Something you're good at
        2. Something that makes you happy
        3. Something you're looking forward to
        4. Something nice someone did for you
        5. Something nice you did for someone else
        Ready? Let's start with something you're good at...
        """
        
        print("OWL response:", exercise)
        tts_play(exercise)
        
        iprompt = [
            {"role": "system", "content": "You are helping a child focus on positive thoughts"},
            {"role": "assistant", "content": exercise},
            {"role": "user", "content": "What's something you're good at?"}
        ]
        
        while True:
            iprompt, text, function_called = self.prepare_message(iprompt, input_type, coping_tools, button=button)
            if function_called in ["story", "stop", "game", "distress"]:
                return function_called 