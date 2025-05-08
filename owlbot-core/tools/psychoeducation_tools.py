from tools.tools import tools

psychoeducation_tools = [
    {
        "type": "function",
        "function": {
            "name": "superheroTrivia",
            "description": "The user would like to play Superhero trivia",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                },
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "geoTrivia",
            "description": " The user would like to play geogrpahy trivia",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                },
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "twentyQuestions",
            "description": " The user would like to play the game twenty questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                },
            },
        }
    }
]
psychoeducation_tools.append(tools[0])
psychoeducation_tools.append(tools[1])
psychoeducation_tools.append(tools[3])

