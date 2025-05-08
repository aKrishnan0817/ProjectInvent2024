from typing import List, Dict, Any
import json

def get_base_tools() -> List[Dict[str, Any]]:
    """Get the base tools for mode switching"""
    return [
        {
            "type": "function",
            "function": {
                "name": "switch_to_game_mode",
                "description": "Switch to game mode to play various games",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "game_type": {
                            "type": "string",
                            "enum": ["twentyQuestions", "superheroTrivia", "geoTrivia"],
                            "description": "The type of game to play"
                        }
                    },
                    "required": ["game_type"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "switch_to_story_mode",
                "description": "Switch to story mode to listen to or generate stories",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "story_type": {
                            "type": "string",
                            "enum": ["default", "random"],
                            "description": "The type of story to play"
                        }
                    },
                    "required": ["story_type"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "switch_to_distress_mode",
                "description": "Switch to distress mode for emergency situations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "Email address for notifications"
                        },
                        "password": {
                            "type": "string",
                            "description": "Email password"
                        },
                        "guardian_email": {
                            "type": "string",
                            "description": "Guardian's email address"
                        }
                    },
                    "required": ["email", "password", "guardian_email"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "switch_to_psychoeducation_mode",
                "description": "Switch to psychoeducation mode to learn about mental health topics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "enum": ["anxiety", "emotions", "coping", "thoughts"],
                            "description": "The psychoeducation topic to learn about"
                        }
                    },
                    "required": ["topic"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "switch_to_coping_mode",
                "description": "Switch to coping mode to learn coping strategies",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "strategy": {
                            "type": "string",
                            "enum": ["breathing", "grounding", "mindfulness", "positive_thoughts"],
                            "description": "The coping strategy to use"
                        }
                    },
                    "required": ["strategy"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "switch_to_stop_mode",
                "description": "Switch to stop mode to end the current session",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    ]

def parse_function_call(function_call: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    """Parse a function call and return the mode name and parameters"""
    if not function_call:
        return None, {}
    
    function_name = function_call.get("name", "")
    arguments = json.loads(function_call.get("arguments", "{}"))
    
    mode_mapping = {
        "switch_to_game_mode": "game",
        "switch_to_story_mode": "story",
        "switch_to_distress_mode": "distress",
        "switch_to_psychoeducation_mode": "psychoeducation",
        "switch_to_coping_mode": "coping",
        "switch_to_stop_mode": "stop"
    }
    
    return mode_mapping.get(function_name), arguments 