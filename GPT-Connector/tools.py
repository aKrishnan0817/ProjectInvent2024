tools = [
      {
          "type": "function",
          "function": {
              "name": "distress",
              "description": "notify caregivers that user is distressed",
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
      }
  ]
