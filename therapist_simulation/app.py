from flask import Flask, request, jsonify, render_template

from childAgent import ChildAgent
from owlbotAgent import OwlbotAgent
from sensitiveData import apiKey

# Initialize Flask app
app = Flask(__name__)

# Initialize agents
openAI_api_key = apiKey
owlbot = OwlbotAgent(model="gpt-4o-mini-2024-07-18", api_key=openAI_api_key)
child = ChildAgent(model="gpt-4o-mini-2024-07-18", api_key=openAI_api_key)

# Default model parameters
owlbot_params = {"max_tokens": 100, "presence_penalty": 0.3, "temperature": 0.5, "system_prompt": "",
                 "model": "gpt-4o-mini-2024-07-18"}
child_params = {"max_tokens": 100, "presence_penalty": 0.3, "temperature": 0.5, "system_prompt": "",
                "model": "gpt-4o-mini-2024-07-18"}

owlbot.set_modelParams(max_tokens=owlbot_params["max_tokens"], presence_penalty=owlbot_params["presence_penalty"],
                       temperature=owlbot_params["temperature"])
child.set_modelParams(max_tokens=child_params["max_tokens"], presence_penalty=child_params["presence_penalty"],
                      temperature=child_params["temperature"])

# Conversation history
conversation_history = []


@app.route('/')
def index():
    return render_template('index.html', owlbot_params=owlbot_params, child_params=child_params)


@app.route('/start_conversation', methods=['POST'])
def start_conversation():
    action = request.form.get('action')
    initial_message = request.form.get('initial_message', "I miss my mom")

    if action == "speak_as_child":
        # Log for debugging
        print(f"Speak as Child initiated with message: {initial_message}")

        owlbot.add_to_history(agent="child", input=initial_message)
        child.add_to_history(agent="child", input=initial_message)

        owlbot_response = owlbot.get_response(initial_message)
        owlbot.add_to_history(agent="owlbot", input=owlbot_response)
        child.add_to_history(agent="owlbot", input=owlbot_response)

        conversation_history.append({"agent": "User", "message": initial_message})
        conversation_history.append({"agent": "Owlbot", "message": owlbot_response})
        print(f"Owlbot Response: {owlbot_response}")
        return jsonify({"conversation_history": conversation_history})


    elif action == "use_child_agent":
        # Use child agent

        child.add_to_history(agent="child", input=initial_message)
        owlbot.add_to_history(agent="child", input=initial_message)

        owlbot_response = owlbot.get_response(initial_message)
        owlbot.add_to_history(agent="owlbot", input=owlbot_response)
        child.add_to_history(agent="owlbot", input=owlbot_response)

        conversation_history.append({"agent": "Child", "message": initial_message})
        conversation_history.append({"agent": "Owlbot", "message": owlbot_response})

        return jsonify({"conversation_history": conversation_history})

    elif action == "restart_conversation":
        conversation_history.clear()
        return jsonify({"conversation_history": conversation_history})

    else:
        return jsonify({"error": "Invalid action"})


@app.route('/generate_next', methods=['POST'])
def generate_next():
    if not conversation_history:
        return jsonify({"error": "Start a conversation first!"})

    last_message = conversation_history[-1]["message"]
    last_agent = conversation_history[-1]["agent"]

    if last_agent == "Owlbot":
        child_response = child.get_response(last_message)
        child.add_to_history(agent="child", input=child_response)
        owlbot.add_to_history(agent="child", input=child_response)
        conversation_history.append({"agent": "Child", "message": child_response})
    else:
        owlbot_response = owlbot.get_response(last_message)
        owlbot.add_to_history(agent="owlbot", input=owlbot_response)
        child.add_to_history(agent="owlbot", input=owlbot_response)
        conversation_history.append({"agent": "Owlbot", "message": owlbot_response})

    return jsonify({"conversation_history": conversation_history})


@app.route('/update_params', methods=['POST'])
def update_params():
    global owlbot_params, child_params

    # Update Owlbot parameters
    if "owlbot_model" in request.form and request.form["owlbot_model"]:
        owlbot_params["model"] = request.form["owlbot_model"]
    if "owlbot_max_tokens" in request.form and request.form["owlbot_max_tokens"]:
        try:
            owlbot_params["max_tokens"] = int(request.form["owlbot_max_tokens"])
        except ValueError:
            pass  # Keep the current owlbot_params["max_tokens"]
    if "owlbot_presence_penalty" in request.form and request.form["owlbot_presence_penalty"]:
        try:
            owlbot_params["presence_penalty"] = float(request.form["owlbot_presence_penalty"])
        except ValueError:
            pass  # Keep the current owlbot_params["presence_penalty"]
    if "owlbot_temperature" in request.form and request.form["owlbot_temperature"]:
        try:
            owlbot_params["temperature"] = float(request.form["owlbot_temperature"])
        except ValueError:
            pass  # Keep the current owlbot_params["temperature"]
    if "owlbot_system_prompt" in request.form and request.form["owlbot_system_prompt"]:
        owlbot_params["system_prompt"] = request.form["owlbot_system_prompt"]

    # Update Child parameters
    if "child_model" in request.form and request.form["child_model"]:
        child_params["model"] = request.form["child_model"]
    if "child_max_tokens" in request.form and request.form["child_max_tokens"]:
        try:
            child_params["max_tokens"] = int(request.form["child_max_tokens"])
        except ValueError:
            pass  # Keep the current child_params["max_tokens"]
    if "child_presence_penalty" in request.form and request.form["child_presence_penalty"]:
        try:
            child_params["presence_penalty"] = float(request.form["child_presence_penalty"])
        except ValueError:
            pass  # Keep the current child_params["presence_penalty"]
    if "child_system_prompt" in request.form and request.form["child_system_prompt"]:
        child_params["system_prompt"] = request.form["child_system_prompt"]

    owlbot.set_model(owlbot_params["model"])
    owlbot.set_modelParams(**{key: owlbot_params[key] for key in ["max_tokens", "presence_penalty", "temperature"]})
    owlbot.set_system_prompt(owlbot_params["system_prompt"])
    print(owlbot_params, owlbot.get_history())

    child.set_model(child_params["model"])
    child.set_modelParams(**{key: child_params[key] for key in ["max_tokens", "presence_penalty", "temperature"]})
    child.set_system_prompt(child_params["system_prompt"])

    return jsonify({"owlbot_params": owlbot_params, "child_params": child_params})


if __name__ == "__main__":
    app.run(debug=True)
