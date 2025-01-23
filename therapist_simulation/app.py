from flask import Flask, request, jsonify, render_template, url_for
from owlbotAgent import OwlbotAgent
from childAgent import ChildAgent
from sensitiveData import apiKey

# Initialize Flask app
app = Flask(__name__)

# Initialize agents
openAI_api_key = apiKey
owlbot = OwlbotAgent(model="gpt-4o-mini-2024-07-18", api_key=openAI_api_key)
child = ChildAgent(model="gpt-4o-mini-2024-07-18", api_key=openAI_api_key)

# Default model parameters
owlbot_params = {"max_tokens": 100, "presence_penalty": 0.3, "temperature": 0.5, "system_prompt": "", "model": "gpt-4o-mini-2024-07-18"}
child_params = {"max_tokens": 100, "presence_penalty": 0.3, "temperature": 0.5, "system_prompt": "", "model": "gpt-4o-mini-2024-07-18"}

owlbot.set_modelParams(max_tokens=owlbot_params["max_tokens"], presence_penalty=owlbot_params["presence_penalty"], temperature=owlbot_params["temperature"])
child.set_modelParams(max_tokens=child_params["max_tokens"], presence_penalty=child_params["presence_penalty"], temperature=child_params["temperature"])

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
    owlbot_params["model"] = request.form.get("owlbot_model", owlbot_params["model"])
    owlbot_params["max_tokens"] = int(request.form.get("owlbot_max_tokens", 100))
    owlbot_params["presence_penalty"] = float(request.form.get("owlbot_presence_penalty", 0.3))
    owlbot_params["temperature"] = float(request.form.get("owlbot_temperature", 0.5))
    owlbot_params["system_prompt"] = request.form.get("owlbot_system_prompt", "")
    owlbot.set_model(owlbot_params["model"])
    owlbot.set_modelParams(**{key: owlbot_params[key] for key in ["max_tokens", "presence_penalty", "temperature"]})
    owlbot.set_system_prompt(owlbot_params["system_prompt"])

    # Update Child parameters
    child_params["model"] = request.form.get("child_model", child_params["model"])
    child_params["max_tokens"] = int(request.form.get("child_max_tokens", 100))
    child_params["presence_penalty"] = float(request.form.get("child_presence_penalty", 0.3))
    child_params["temperature"] = float(request.form.get("child_temperature", 0.5))
    child_params["system_prompt"] = request.form.get("child_system_prompt", "")
    child.set_model(child_params["model"])
    child.set_modelParams(**{key: child_params[key] for key in ["max_tokens", "presence_penalty", "temperature"]})
    child.set_system_prompt(child_params["system_prompt"])

    return jsonify({"owlbot_params": owlbot_params, "child_params": child_params})

if __name__ == "__main__":
    app.run(debug=True)