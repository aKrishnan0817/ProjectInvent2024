from typing import List, Dict, Any, Tuple
from tools.base_tools import get_base_tools, parse_function_call

def prepare_message(
    iprompt: List[Dict[str, str]],
    input_type: int,
    button: str = None
) -> Tuple[List[Dict[str, str]], str, str]:
    """
    Prepare a message for processing and handle mode switching.
    
    Args:
        iprompt: List of message dictionaries
        input_type: Type of input (1 for text, 2 for voice)
        button: Optional button press
        
    Returns:
        Tuple of (updated iprompt, text response, function called)
    """
    # Add system prompt for mode switching
    system_prompt = {
        "role": "system",
        "content": """You are an AI assistant that helps children. 
        You can switch between different modes based on the child's needs.
        Available modes are:
        - game: Play games like 20 questions, superhero trivia, or geography trivia
        - story: Listen to or generate stories
        - distress: Get help in emergency situations
        - psychoeducation: Learn about mental health topics
        - coping: Learn coping strategies
        - stop: End the current session
        
        If the child wants to switch modes, use the appropriate function call.
        Otherwise, continue the conversation naturally."""
    }
    
    if iprompt[0]["role"] != "system":
        iprompt.insert(0, system_prompt)
    
    # Get tools for mode switching
    tools = get_base_tools()
    
    # Process the message and get response
    # This would be replaced with actual API call to the model
    response = {
        "content": "I understand you want to switch modes.",
        "function_call": {
            "name": "switch_to_game_mode",
            "arguments": '{"game_type": "twentyQuestions"}'
        }
    }
    
    # Parse function call if present
    mode_name, params = parse_function_call(response.get("function_call"))
    
    if mode_name:
        return iprompt, response["content"], mode_name
    
    return iprompt, response["content"], None

def get_mode_switch_prompt(mode: str) -> str:
    """Get a prompt for switching to a specific mode"""
    prompts = {
        "game": "Would you like to play a game? We can play 20 questions, superhero trivia, or geography trivia.",
        "story": "Would you like to listen to a story or create a new one?",
        "distress": "I notice you might be feeling distressed. Would you like to talk about it?",
        "psychoeducation": "Would you like to learn about anxiety, emotions, coping skills, or thoughts?",
        "coping": "Would you like to learn some coping strategies?",
        "stop": "Would you like to end our conversation?"
    }
    return prompts.get(mode, "How can I help you?") 