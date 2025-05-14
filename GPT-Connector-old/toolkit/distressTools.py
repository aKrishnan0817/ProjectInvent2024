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

from toolkit.tools import tools

distressConversationTools = []
distressConversationTools.append(tools[1])
distressConversationTools.append(tools[2])
distressConversationTools.append(tools[3])
