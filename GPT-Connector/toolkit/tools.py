tools = [
      {
          "type": "function",
          "function": {
              "name": "distress",
              "description": "the user explicity, clearly, and directly states that they are in a severe state of distress and needs urgent consoling.",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "Example return",
                      },
                      #"unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                  },

                  #"required": ["location"],
              },
          }
      },
      {
          "type": "function",
          "function": {
              "name": "story",
              "description": "the user wants to listen to a story",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "Example return",
                      },
                      #"unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                  },

                  #"required": ["location"],
              },
          }
      },
      {
          "type": "function",
          "function": {
              "name": "game",
              "description": "plays a game with the user",
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
              "name": "stop",
              "description": "the user wants to stop having this conversation",
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
              "name": "coping",
              "description": "the user would like to practice coping skills such as meditation or breathing excerises",
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
