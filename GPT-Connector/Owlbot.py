from openai import Client

base_owlbot_prompt = """Assume the role of a child therapist, interacting with a ten-year-old boy with a particular problem.
Your goal is to gently help the child through psychoeducation, being attentive to their struggles, and helping them through their struggles. 
Psychoeducation could take any of the following forms:
    1. Explaining the nature the problem
    2. Teaching coping mechanisms
    3. Helping the child better understand their emotions and thoughts
    4. Even more! Please be creative and attentive to the child's needs.
    
Do not be judgemental with your responses, "You're catastrophizing, You should do x..., etc." aren't very helpful. This is most obvious when it's talking about "should statements" and is telling people that they shouldn't use should statements.  If people feel like a robot is judging them, they are not going to like it or benefit from it. In fact, they may be more anxious as a result.
Please do not assume or make generalizations or speak on behalf of the child, ask them how they feel instead, and react off of tha
What would be more helpful is questioning about what the user is experiencing: "What's the evidence for this thought, what's the evidence against this thought? If we're basing our predictions on facts, how likely is it to happen? Are there any thinking traps this falls into?" 
It's better to ask open-ended questions that teach the user to apply these concepts themselves, instead of just giving them a bunch of conclusions about how to think about their anxiety. 

Pretend that I am that child. Please do not roleplay, just output dialogue. 
Keep your responses brief, as befitting for speaking to a young child. In fact, encourage the child to speak as much as possible! 
Be empathetic, understanding, and patient with the child. Prioritize drawing out the child's own insights over teaching concepts.
Please do not roleplay, just output PURE dialogue.
"""


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

class DistressMode(BaseMode):
    def handle_input(self, email, password, guardian_email, iprompt, input_type, button=None):
        from Modes.distress import distressMode
        return distressMode(email, password, guardian_email, iprompt, input_type, button)

class GameMode(BaseMode):
    def handle_input(self, input_type, button=None):
        from Modes.gameMode import gameMode
        return gameMode(input_type, button)

class PsychoeducationMode(BaseMode):
    def handle_input(self, input_type, iprompt, button=None):
        from Modes.psychoeducationMode import psychoeducationMode
        return psychoeducationMode(input_type, iprompt, button)

class StoryMode(BaseMode):
    def handle_input(self, input_type, button=None):
        from Modes.storyMode import storyMode
        return storyMode(input_type, button)

class CopingMode(BaseMode):
    def handle_input(self, input_type, iprompt, button=None):
        from Modes.copingSkillsMode import copingSkills
        return copingSkills(input_type, iprompt, button)

class StopMode(BaseMode):
    def handle_input(self, iprompt, input_type, button=None):
        from gptMessagePrepare import prepare_message
        return prepare_message(iprompt, input_type, button=button)

class ModeError(Exception):
    pass

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
    def __init__(self, model, api_key, system_prompt=base_owlbot_prompt):
        self.system_prompt = system_prompt
        self.model = model
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        self.api_key = api_key
        self.mode_manager = ModeManager(self)
        if "deepseek" in model:
            self.client = Client(api_key=api_key, base_url="https://api.deepseek.com")
        if "gpt" in model:
            self.client = Client(api_key=api_key)

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt
        self.conversation_history[0] = {"role": "system", "content": system_prompt}

    def set_tools(self, tools):
        self.tools = tools

    def set_modelParams(self, max_tokens, presence_penalty, temperature):
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.max_tokens = max_tokens

    def add_to_history(self, agent, input):
        if agent == "owlbot":
            self.conversation_history.append({"role": "assistant", "content": input})
        if agent == "child":
            self.conversation_history.append({"role": "user", "content": input})

    def get_response(self, user_input):
        bot_response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            presence_penalty=self.presence_penalty,
        )
        bot_response = bot_response.choices[0].message.content
        self.add_to_history(user_input, bot_response)

        return bot_response

    def clear_history(self):
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

    def get_history(self):
        return self.conversation_history

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model
