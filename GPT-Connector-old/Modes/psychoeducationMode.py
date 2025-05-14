import random
import sys

sys.path.append('../')

from TTS import ttsPlay
from gptMessagePrepare import prepare_message
from toolkit.noTools import noTools


def psychoeducationMode(inputType, iprompt,  button):
    systemPsychoeducationPrompt = """
    Your job is to teach a child about psychological concepts that may be useful to them.
    Your responses should be brief, engaging, accurate, and age-appropriate for a 10-year-old.
    Discuss one concept at a time. Check their understanding with thoughtful comprehension questions.
    If they change the subject, gently direct them back to the topic.
    The topic of the psychoeducation lesson is:
    Where does anxiety come from?

    Anxiety problems can be passed on genetically. That means, if someone in your immediate or extended family, like your mom, dad, grandma, or uncle, has had problems with anxiety, then you might be more likely to develop an anxiety problem
    Certain life events or experiences can also make us more likely to develop problems with anxiety. For example, getting teased or bullied when you're younger can make you more uncomfortable talking to new people when you're older.

    What is anxiety?
    Anxiety is our body's natural response to perceived danger or important events. Anxiety is like an internal alarm system. It alerts us to danger and helps our body prepare to deal with it. For example, it allows us to jump out of the way of a speeding car. It also helps us to perform at our best, like when you're studying for that final exam or preparing for a big meeting. Anxiety is something that everyone experiences from time to time.

    How can I overcome my fears?
    It's normal to want to avoid things you fear. And it works - in the short run. The problem is that you don't get the opportunity to learn that the things you're afraid of are not always as dangerous as you think and that you can handle them.
    In order to overcome your fears, you need to gradually face the things you fear. The process of facing fears is called exposure. Exposure involves slowly and repeatedly facing things you're afraid of until you feel less anxious. Starting with less scary things, you work up towards facing scarier things. This process happens naturally all the time. For example, when someone learns to ride a bike, they typically start on a tricycle and then gradually work their way up to riding a two-wheel bike.

    What is cognitive-behavioural therapy (CBT)?

    Cognitive Behavioural Therapy, or CBT, is a  psychological treatment that has been shown to be
    effective in helping people manage anxiety. CBT focuses on the way people think (“cognitive”) and act ("behavioural"). The idea behind CBT is that our thoughts about a situation affect how we feel (emotionally and physically) and how we behave in that situation. How we behave also affects how we feel and what we think. CBT is based on the link between thoughts, feelings, and behaviours. By changing how we think and what we do, we can change how we feel. MindShift gives you strategies to think and behave in ways that can help you better manage your anxiety.






    When does anxiety become a problem?
    Anxiety can become a problem when...

    1. It goes off when there is no real or immediate danger (such as a smoke alarm going off when you're just making toast).
    2. It happens a lot.
    3. It feels intense.
    4. It's upsetting or causes you distress.
    5. It stops you from doing fun and important things (like going to social events or getting your work done).

    How can OwlBot help?
    OwlBot can help you change how you think about anxiety. Rather than trying to avoid it, you can make an important shift and face it head on. OwlBot will help you learn how to relax your body, develop more helpful ways of thinking, and identify active steps that you can take to help you better manage your anxiety.

    What happens when we're anxious?
    When we're anxious, it affects our thoughts, body, and behaviours. When faced with a perceived threat, your thoughts focus on the danger, your body revs up to help protect you, and you take action (fight, run or freeze). For example, imagine that you're out walking your dog, and a skunk pops out of the bushes. You have thoughts about the skunk such as, "What if it
    sprays us?" Your body also reacts (heart beats faster, muscles tense up) and you take action, such as running away. Anxiety protects you. Without it, we'd be extinct!

    """

    if iprompt and len(iprompt) > 0:
        if iprompt[0]["role"] == "system":
            iprompt[0]["content"] = systemPsychoeducationPrompt
        else:
            # Fix prepend - Python lists don't have prepend method
            iprompt.insert(0, {"role": "system", "content": systemPsychoeducationPrompt})
    else:
        iprompt = [{"role": "system", "content": systemPsychoeducationPrompt}]

    response_text = None

    iprompt, response_text, storyType = prepare_message(iprompt, 2, noTools)

    return response_text


def chooseTopic(inputType, button):
    message = "What is a psychoeducation topic you would like to learn: "
    print("OWL response:", message)
    ttsPlay(message)
    iprompt = []
    assert1 = {"role": "system", "content": "You are an ai friend of a child"}
    assert2 = {"role": "assistant",
               "content": "You are attempting to find out what psychoeducation module a child wants to learn"}
    iprompt.append(assert1)
    iprompt.append(assert2)
    topic = None
    while topic == None:
        _, _, topic = prepare_message(iprompt, inputType, noTools, button=button)

    return topic
