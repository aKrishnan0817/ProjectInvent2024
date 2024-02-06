def get_matthew_bot_response(client, **kwargs):
    system = kwargs["system"]
    chat_history = kwargs["chat_history"]
    user_input = kwargs["user_input"]
    output = client.chat.completions.create(model="gpt-4",
                                            temperature=1,
                                            presence_penalty=0,
                                            frequency_penalty=0,
                                            max_tokens=2000,
                                            messages=[
                                                {"role": "system", "content": f"{system}. Conversation history: {chat_history}"}, #In order to properly train it I need to be able to signal where a conversation ends and where one begins. I should probably look into this later
                                                {"role": "assistant", "content": "Jonah, let's talk about another coping skill"}, #this shouldn't be the very start of coping mode. Perhaps I may need to see how the decision making mode is progressing in order to
                                                {"role": "user", "content": "Ok"},
                                                {"role": "assistant", "content": "This is a relaxation script used for calming yourself down. Do you want me to show it to you?"},
                                                {"role": "user", "content": "Yes"},
                                                {"role": "assistant", "content": "I'm going to ask you to relax. In a few minutes, I am going to say some things that I hope will help you create a picture in your mind... I am also going to ask you to relax different parts of your body. Learning to relax will help you cope with angry, sad, and scary feelings. Find a comfortable position in your chair, not touching anyone, and take in a few relaxing breaths... Close your eyes and relax... Wiggle a little bit and make yourself comfortable... Alright, take a few relaxing breaths... breathe in... and breathe out... breath in... and breath out. That's it -- you are feeling peaceful. If you were angry, you can picture yourself moving from hot to cold on the thermometer. Becoming more and more relaxed, cold, peaceful. Now, with your eyes closed, pretend you are on a white fluffy cloud, high in the sky on a beautiful day. You are floating peacefully on that white fluffy cloud... moving very slowly... you are as light as a feather... and the fluffy cloud holds you safely... floating across the sky. Now, as I count from 1 to 3, imagine that you are sinking deeper and deeper into that cloud...so the cloud is all around you. 1... 2... 3. You are enjoying the ride on the cloud. Now, notice on your toes and feet, how relaxed they feel... notice your legs...all the muscles on your legs are light and relaxed on the cloud...notice your arms... Notice your necks... notice your head... now you are totally relaxed... floating on the fluffy cloud... Remember that you can return to your very own cloud whenever you feel like you need to calm down and relax... Whenever you need to cool off... move from hot to cool on the thermometer... Now, we are getting ready to stop our ride on the cloud. We will stop on the count of three...1...2...3... Open your eyes and stretch a little..... How was that? Do you wish to continue?"},
                                                {"role": "user", "content": "Yes, it was good"},
                                                {"role": "assistant", "content": "Jonah, let's talk about another coping skill"}, #this shouldn't be the very start of coping mode
                                                {"role": "user", "content": "Ok"},
                                                {"role": "assistant", "content": "This is a relaxation script used for calming yourself down. Do you want me to show it to you?"},
                                                {"role": "user", "content": "Yes"},
                                                {"role": "assistant", "content": "I'm going to ask you to relax. In a few minutes, I am going to say some things that I hope will help you create a picture in your mind... I am also going to ask you to relax different parts of your body. Learning to relax will help you cope with angry, sad, and scary feelings. Find a comfortable position in your chair, not touching anyone, and take in a few relaxing breaths... Close your eyes and relax... Wiggle a little bit and make yourself comfortable... Alright, take a few relaxing breaths... breathe in... and breathe out... breath in... and breath out. That's it -- you are feeling peaceful. If you were angry, you can picture yourself moving from hot to cold on the thermometer. Becoming more and more relaxed, cold, peaceful. Now, with your eyes closed, pretend you are on a white fluffy cloud, high in the sky on a beautiful day. You are floating peacefully on that white fluffy cloud... moving very slowly... you are as light as a feather... and the fluffy cloud holds you safely... floating across the sky. Now, as I count from 1 to 3, imagine that you are sinking deeper and deeper into that cloud...so the cloud is all around you. 1... 2... 3. You are enjoying the ride on the cloud. Now, notice on your toes and feet, how relaxed they feel... notice your legs...all the muscles on your legs are light and relaxed on the cloud...notice your arms... Notice your necks... notice your head... now you are totally relaxed... floating on the fluffy cloud... Remember that you can return to your very own cloud whenever you feel like you need to calm down and relax... Whenever you need to cool off... move from hot to cool on the thermometer... Now, we are getting ready to stop our ride on the cloud. We will stop on the count of three...1...2...3... Open your eyes and stretch a little..... How was that? Do you wish to continue?"},
                                                {"role": "user", "content": "I didn't like it"},
                                                {"role": "assistant", "content": "Why didn't you? Is there anything I can do to help?"},
                                                {"role": "user", "content": "I thought it was too childish and pointless"},
                                                {"role": "assistant", "content": "That's alright, do you want another script?"},
                                                {"role": "user", "content": "Yes"},
                                                {"role": "assistant", "content": "[Another script goes here]"},


                                            ])



                                            #this would be just the code for coping mode
                                            #this should open somewhat regularly independent of jonah and whenever jonah asks himself
                                            #ask for how often it should open(whether its completly random, set times(like once a day), etc.)
                                            #How this would work:
                                            #Cycle through saying preset(or just very similar) specific coping skills for general scenarios
                                            #Frequently ask Jonah to interact with the coping skills himself
                                            #This is intended to be more of a conversation-based mode so it shouldn't be absolutely preset
                                            #Ex:
                                            #Hello Jonah, this is one coping skill, this is where you would use it and what it is best for, and this is how you would use it
                                            #Would you like to try it yourself?
                                            #(Jonah tries it out)
                                            #If he does well:
                                            #Do you have any further questions?
                                            #If he doesn't do it perfectly or asks some questions:
                                            #Question answer/advice to help jonah in the future
                                            #Jonah, do you want to learn and practice another coping skill?
                                            #If yes, repeat process a couple times
                                            #If no, return to conversation mode and shorten the timer for the next time coping skills mode is activated

    chatgpt_output = ""
    if output.choices:
        # Accessing the content attribute directly
        chatgpt_output = output.choices[0].message.content

    return chatgpt_output

