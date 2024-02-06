

# Import necessary libraries
from flask import Flask, render_template, request, redirect
from openai import OpenAI


import os
import time
import sys
sys.path.append('../')
import sensitiveData
client = OpenAI(api_key=sensitiveData.apiKey)
from aaron import get_aaron_bot_response
from anya import get_anya_bot_response
from atul import get_atul_bot_response
from dimitri import get_dimitri_bot_response
from forrest import get_forrest_bot_response
from matthew import get_matthew_bot_response
from tanner import get_tanner_bot_response
from karan import get_karan_bot_response
from zach import get_zach_bot_response
from zoe import get_zoe_bot_response
from j import get_j_bot_response
from taiwo import get_taiwo_bot_response
from val import get_val_bot_response

# setting path

#from urllib.parse import quote as url_quote

# Define the name of the bot
name = 'BOT'

# Define the role of the bot
role = 'friend'

# Define the impersonated role with instructions
impersonated_role = f"""
    From now on, you are going to act as {name}. Your role is {role}.
    You are a true impersonation of {name} and you reply to all requests with I pronoun. Your role is to play a game called 20 questions where you come up with a random thing and the user has 20 questions to try and guess what it is.
    """
    # Your role is to play a game in which the user picks a catagory and your responses must always be one word in that category. The last letter of the users word must be the first letter of your word.


# Initialize variables for chat history
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd()
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

# Initialize chat history
chat_history = ''

# Create a Flask web application
app = Flask(__name__)

def chatcompletion(user_input, system, chat_history):
    output = client.chat.completions.create(model="gpt-3.5-turbo-0301",
                                            temperature=1,
                                            presence_penalty=0,
                                            frequency_penalty=0,
                                            max_tokens=2000,
                                            messages=[
                                                {"role": "system", "content": f"{system}. Conversation history: {chat_history}"},
                                                {"role": "user", "content": f"{user_input}"},
                                            ])

    chatgpt_output = ""
    if output.choices:
        # Accessing the content attribute directly
        chatgpt_output = output.choices[0].message.content

    return chatgpt_output


# Function to handle user chat input
def chat(system, chat_history, user_input):
    global name, chatgpt_output

    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chatgpt_raw_output = chatcompletion(user_input, system, chat_history)
    chatgpt_output = f'{name}: {chatgpt_raw_output}'

    with open(history_file, 'a') as f:
        f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output

# Function to get a response from the chatbot
def get_response(system, history, userText):
    return chat(system, history, userText)

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

# Define app routes
@app.route("/zach")
def zach():
    return render_template("zach.html")

# Define app routes
@app.route("/aaron")
def aaron():
    return render_template("aaron.html")

# Define app routes
@app.route("/karan")
def karan():
    return render_template("karan.html")

# Define app routes
@app.route("/dimitri")
def dimitri():
    return render_template("dimitri.html")

# Define app routes
@app.route("/atul")
def atul():
    return render_template("atul.html")

# Define app routes
@app.route("/forrest")
def forrest():
    return render_template("forrest.html")

# Define app routes
@app.route("/anya")
def anya():
    return render_template("anya.html")

# Define app routes
@app.route("/zoe")
def zoe():
    return render_template("zoe.html")

# Define app routes
@app.route("/tanner")
def tanner():
    return render_template("tanner.html")

# Define app routes
@app.route("/matthew")
def matthew():
    return render_template("matthew.html")

# Define app routes
@app.route("/j")
def j():
    return render_template("j.html")

# Define app routes
@app.route("/val")
def val():
    return render_template("val.html")

# Define app routes
@app.route("/taiwo")
def taiwo():
    return render_template("taiwo.html")



@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    history = request.args.get("history")
    system = request.args.get("system")
    return str(get_response(system, history, userText))

@app.route("/aaron_get")
# Function for the bot response
def get_aaron_response():
    global client
    all_args = request.args.to_dict()
    return str(get_aaron_bot_response(client, **all_args))


@app.route("/anya_get")
# Function for the bot response
def get_anya_response():
    global client
    all_args = request.args.to_dict()

    return str(get_anya_bot_response(client, **all_args))


@app.route("/atul_get")
# Function for the bot response
def get_atul_response():
    global client
    all_args = request.args.to_dict()

    return str(get_atul_bot_response(client, **all_args))


@app.route("/dimitri_get")
# Function for the bot response
def get_dimitri_response():
    global client
    all_args = request.args.to_dict()

    return str(get_dimitri_bot_response(client, **all_args))


@app.route("/forrest_get")
# Function for the bot response
def get_forrest_response():
    global client
    all_args = request.args.to_dict()

    return str(get_forrest_bot_response(client, **all_args))


@app.route("/matthew_get")
# Function for the bot response
def get_matthew_response():
    global client
    all_args = request.args.to_dict()

    return str(get_matthew_bot_response(client, **all_args))


@app.route("/karan_get")
# Function for the bot response
def get_karan_response():
    global client
    all_args = request.args.to_dict()

    return str(get_karan_bot_response(client, **all_args))


@app.route("/tanner_get")
# Function for the bot response
def get_tanner_response():
    global client
    all_args = request.args.to_dict()

    return str(get_tanner_bot_response(client, **all_args))


@app.route("/zach_get")
# Function for the bot response
def get_zach_response():
    global client
    all_args = request.args.to_dict()

    return str(get_zach_bot_response(client, **all_args))


@app.route("/zoe_get")
# Function for the bot response
def get_zoe_response():
    global client
    all_args = request.args.to_dict()

    return str(get_zoe_bot_response(client, **all_args))



@app.route("/j_get")
# Function for the bot response
def get_j_response():
    global client
    all_args = request.args.to_dict()
    # Pass all arguments as keyword arguments
    return str(get_j_bot_response(client, **all_args))


@app.route("/taiwo_get")
# Function for the bot response
def get_taiwo_response():
    global client
    all_args = request.args.to_dict()

    return str(get_taiwo_bot_response(client, **all_args))


@app.route("/val_get")
# Function for the bot response
def get_val_response():
    global client
    all_args = request.args.to_dict()

    return str(get_val_bot_response(client, **all_args))


@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

# Run the Flask app
if __name__ == "__main__":
    app.run()
