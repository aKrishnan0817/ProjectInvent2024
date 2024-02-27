from toolkit.tools import tools


selectGameTools = [
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
selectGameTools.append(tools[0])
selectGameTools.append(tools[1])
selectGameTools.append(tools[3])

triviaTools = []
triviaTools.append(tools[0])
triviaTools.append(tools[1])
triviaTools.append(tools[3])
