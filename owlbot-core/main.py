import os
from core.owlbot import OwlbotAgent
from utils.message_prepare import prepare_message
from utils.pi_components import PiComponents
from config.sensitive_data import email, password, guardian_email

def handle_mode_switch(current_mode, owlbot, iprompt, input_type, button):
    """Handle the mode switching logic"""
    if current_mode:
        result = owlbot.mode_manager.switch_mode(
            current_mode,
            email=email,
            password=password,
            guardian_email=guardian_email,
            iprompt=iprompt,
            input_type=input_type,
            button=button
        )
        return result
    return None

def main():
    # Initialize Owlbot agent
    owlbot = OwlbotAgent(
        model="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY"),
        system_prompt="You are a friend of a nine year old boy. You are to act and talk the way a younger child would to his friends"
    )

    # Initialize components
    input_type = 0  # 1 for typing, 0 for speaking
    button = PiComponents(button_pin=2, led_pin=4)
    
    # Initialize conversation
    iprompt = []
    current_mode = None
    previous_mode = None
    
    while True:
        try:
            # Get new mode if we're not in a mode or if we're ready to switch
            if previous_mode == current_mode:
                iprompt, text, current_mode = prepare_message(iprompt, input_type, button=button)
            
            previous_mode = current_mode
            
            # Handle mode switching
            result = handle_mode_switch(current_mode, owlbot, iprompt, input_type, button)
            if result:
                current_mode = result
                
        except Exception as e:
            print(f"Error in main loop: {e}")
            # Reset to default state
            current_mode = None
            previous_mode = None
            continue

if __name__ == "__main__":
    main() 