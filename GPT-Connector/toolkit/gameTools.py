selectGameTools = [
      {
          "type": "function",
          "function": {
              "name": "movieTrivia",
              "description": "The user would like to play movie trivia",
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
