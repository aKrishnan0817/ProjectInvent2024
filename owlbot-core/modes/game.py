from modes.base import BaseMode
import random

class GameMode(BaseMode):
    def __init__(self, owlbot_agent):
        super().__init__(owlbot_agent)
        self.games = {
            "twentyQuestions": self._play_20_questions,
            "superheroTrivia": self._play_superhero_trivia,
            "geoTrivia": self._play_geo_trivia
        }

    def handle_input(self, input_type, button=None):
        game = self._choose_game(input_type, button)
        if game in self.games:
            return self.games[game](input_type, button)
        return game  # Return the mode name if it's a mode switch

    def _choose_game(self, input_type, button):
        message = "What game would you like to play? We can play 20 questions, Superhero Trivia or geography trivia."
        self.speak(message)
        
        iprompt = [
            {"role": "system", "content": "You are an ai friend of a child"},
            {"role": "assistant", "content": "You are attempting to find out whether a child wants to play 20 questions, Superhero Trivia or geography trivia."}
        ]
        
        game = None
        while game is None:
            _, _, game = self.prepare_message(iprompt, input_type, button=button)
        return game

    def _play_20_questions(self, input_type, button):
        secret_object_type = random.choice(["animal", "plant", "inanimate object", "historical person"])
        secret_object_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        secret_object_question = f"Choose a random example of a {secret_object_type}. It should start with the letter: {secret_object_letter}. Your response should be a single word and nothing else. Do not tell the user what the object is unless explicitly said so. Only respond yes or no."

        iprompt = [
            {"role": "system", "content": "You are still waiting to decide what your secret object is."},
            {"role": "assistant", "content": secret_object_question}
        ]

        first_message = "Let's play 20 questions. I've thought of a word and you need to guess it."
        self.speak(first_message)

        while True:
            iprompt, text, function_called = self.prepare_message(iprompt, input_type, button=button)
            if function_called in ["story", "stop", "distress", "coping"]:
                return function_called

    def _play_superhero_trivia(self, input_type, button):
        list_of_superheroes = ["Superman", "Spiderman", "Iron Man", "Wonder Woman", "Batman", "Aquaman", 
                             "Captain America", "Incredible Hulk", "Thor", "Ant-Man", "Wolverine"]
        random_superhero = random.choice(list_of_superheroes)

        content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{random_superhero}", superheroes and superhero movies. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorrect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""

        iprompt = [
            {"role": "system", "content": "You are an ai friend to a child"},
            {"role": "assistant", "content": content},
            {"role": "user", "content": "Please ask me a question and remember to only ask me questions!"}
        ]

        iprompt, text, function_called = self.prepare_message(iprompt, 2, button=button)
        
        while True:
            random_superhero = random.choice(list_of_superheroes)
            content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{random_superhero}", superheroes and superhero movies. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorrect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""
            
            iprompt[1] = {"role": "assistant", "content": content}
            iprompt, text, function_called = self.prepare_message(iprompt, input_type, button=button)
            
            if function_called in ["story", "stop", "distress", "coping"]:
                return function_called

    def _play_geo_trivia(self, input_type, button):
        from ..utils.file_utils import read_file_and_tokenize
        geo_topic_list = read_file_and_tokenize("modes/game_mode_topics.txt")
        random_geo_topic = random.choice(geo_topic_list)

        content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{random_geo_topic}", and geography topics. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorrect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""

        iprompt = [
            {"role": "system", "content": "You are an ai friend to a child"},
            {"role": "assistant", "content": content},
            {"role": "user", "content": "Please ask me a question and remember to only ask me questions!"}
        ]

        iprompt, text, function_called = self.prepare_message(iprompt, 2, button=button)
        
        while True:
            random_geo_topic = random.choice(geo_topic_list)
            content = f"""You are now a trivia show host. Your job is to ask the child interesting trivia questions about "{random_geo_topic}", and geography topics. When the child asks to start the game starts and you respond with one such trivia question. If the child gets the answer right, you say correct! And then ask the next question, if they get it wrong, give the child a hint and wait for their next response if their next response is correct, say correct! and ask the next question, if their next response is still incorrect, just give the child another hint until they answer correctly. If after answering the question incorrectly the child says 'i give up', move on to the next question. you may never ever ever repeat questions"""
            
            iprompt[1] = {"role": "assistant", "content": content}
            iprompt, text, function_called = self.prepare_message(iprompt, input_type, button=button)
            
            if function_called in ["story", "stop", "distress", "coping"]:
                return function_called 