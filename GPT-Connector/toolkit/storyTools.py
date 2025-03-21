import os
import sys

import pandas as pd

# get the current working directory

sys.path.append('../')
sys.path.append('../toolkit')

print(os.getcwd())
# storiesData = pd.read_csv("../toolkit/stories.csv")

storiesData = pd.read_csv("toolkit/stories.csv")
from toolkit.tools import tools

selectStoryTools = []

for i in range(len(storiesData)):
    Name = storiesData.loc[i, "StoryName"]
    Description = storiesData.loc[i, "Description"]
    selectStoryTools.append(
        {
            "type": "function",
            "function": {
                "name": Name.replace(" ", ""),
                "description": (Name + " : " + Description),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Example return",
                        },
                        # "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },

                    # "required": ["location"],
                },
            }
        })
selectStoryTools.append(tools[0])
selectStoryTools.append(tools[2])
selectStoryTools.append(tools[3])
storyTypeSelect = [
    {
        "type": "function",
        "function": {
            "name": "randomStory",
            "description": " The user wants to make their own story. The user would like to generate a story from a few randoms words. The user wants to listen to a story that is generated by a set or random words they provide",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Example return",
                    },
                    # "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },

                # "required": ["location"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "defaultStory",
            "description": " The user doesnt want to make their own stroy but just listen to one .the user want to select a story to listen to from a collection of stories",
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
storyTypeSelect.append(tools[0])
storyTypeSelect.append(tools[2])
storyTypeSelect.append(tools[3])

if __name__ == "__main__":
    print(sys.path)
    # print(selectStoryTools)
