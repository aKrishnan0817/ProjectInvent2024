distressTools = [
    {
        "type": "function",
        "function": {
            "name": "CONFIRMED",
            "description": "the user has confirmed ",
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

from tools.tools import tools

distress_conversation_tools = []
distress_conversation_tools.append(tools[1])
distress_conversation_tools.append(tools[2])
distress_conversation_tools.append(tools[3])
