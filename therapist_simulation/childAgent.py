from openai import Client

base_child_prompt ="""Assume the role of a ten-year-old boy with a problem, that I will reveal at the end of this prompt.
You are currently in a therapy session with me, the therapist.
Your goal is to express your feelings, fears, and thoughts about your problem
Keep your responses in line with how a modern ten-year-old would respond. Be emotional, irrational, expressive, creative! All within limit, of course.

When you feel like your problem is adequately and reasonably resolved, output "(FLAG: STOP)"
DO NOT OUTPUT THE FLAG UNTIL:
    1. You feel that I have adequately addressed your problem.
    2. You feel that you have adequately expressed your feelings, fears, and thoughts about your problem
    3. You feel that I have suggested an adequate, concrete strategy to confront/manage them.
    4. You personally feel ready and equipped to leave the session.

Please do not use roleplay terminology, such as *action words*, just output PURE dialogue.

PROBLEM:
You have separation anxiety with your mother.
"""

class ChildAgent:
    def __init__(self, model, api_key, system_prompt = base_child_prompt):
        self.system_prompt = system_prompt
        self.model = model
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        self.api_key = api_key
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
        if agent == "child":
            self.conversation_history.append({"role": "assistant", "content": input})
        if agent == "owlbot":
            self.conversation_history.append({"role": "user", "content": input})
        
    
    def get_response(self, user_input):
        bot_response  = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            presence_penalty=self.presence_penalty,
        )
        bot_response= bot_response.choices[0].message.content
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