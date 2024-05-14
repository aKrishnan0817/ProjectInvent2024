
from openai import OpenAI
import random
import sys

sys.path.append('../')

from TTS import ttsPlay
from gptMessagePrepare import prepare_message

from toolkit.noTools import noTools
from toolkit.tools import tools





def copingSkills(inputType,iprompt, button):
    iprompt=[
        {"role": "system", "content": f"You are an AI friend to a 9 year old who needs help with coping skills. Conversation history: {iprompt}"}, #In order to properly train it I need to be able to signal where a conversation ends and where one begins. I should probably look into this later
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
    ]

    copingTools = tools[:len(tools)-1]
    #generate first message
    iprompt,text,functionCalled=prepare_message(iprompt,2,noTools)


    while True:
        iprompt,text,functionCalled=prepare_message(iprompt,inputType,copingTools,button=button) #preparing the messages for ChatGPT

        if functionCalled in ["story","stop","distress"]:
            return functionCalled
