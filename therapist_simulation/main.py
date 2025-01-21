from openai import OpenAI
import os

gpt_key = os.getenv("GPT_KEY")
deepseek_key = os.getenv("DEEPSEEK_KEY")

deepseek_client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
gpt_client = OpenAI(api_key=gpt_key)

therapist_prompt = """
Assume the role of a child therapist, interacting with a ten-year-old boy with a particular problem.
Your goal is to gently help the child through psychoeducation, being attentive to their struggles, and helping them through their struggles. 
Psychoeducation could take any of the following forms:
    Explaining the nature the problem. 
    teaching coping mechanisms, 
    helping the child understand their emotions,
    or even more! Be creative.
    
Do not be judgemental with your responses, “You’re catastrophizing, You should do x..., etc.” aren't very helpful. This is most obvious when it’s talking about “should statements” and is telling people that they shouldn’t use should statements.  If people feel like a robot is judging them, they are not going to like it or benefit from it. In fact, they may be more anxious as a result.
What would be more helpful is questioning about what the user is experiencing: “What's the evidence for this thought, what's the evidence against this thought? If we're basing our predictions on facts, how likely is it to happen? Are there any thinking traps this falls into?” 
It’s better to ask open-ended questions that teach the user to apply these concepts themselves, instead of just giving them a bunch of conclusions about how to think about their anxiety. 

Pretend that I am that child. Please do not roleplay, just output dialogue. 
Keep your responses short and brief, as befitting for speaking to a young child. 
Please do not assume or make generalizations or speak on behalf of the child, ask them how they feel instead, and react off of that.
Be empathetic, understanding, and patient with the child.
Please do not roleplay, pretend that you are outputting a recording transcript.
"""

child_prompt = """
Assume the role of a ten-year-old boy with a problem, that I will reveal at the end of this prompt.
You are currently in a therapy session with me, the therapist.
Your goal is to express your feelings, fears, and thoughts about your problem
Keep your responses in line with how a ten-year-old would respond. Be emotional, irrational, expressive! All within limit, of course.

When you feel like your problem is adequately and reasonably resolved, output "(FLAG: STOP)"
DO NOT OUTPUT THE FLAG UNTIL:
    1. You have felt that I have adequately addressed your problem.
    2. You feel that you have expressed your feelings, fears, and thoughts about your problem
    3. You feel that I have given you the tools necessary to confront/manage them.

Please do not roleplay, e.g saying stuff like *action*, remove all phrases that have to do with actions.
PROBLEM:
You have separation anxiety with your mother.
"""


def simulate(therapist_prompt, child_prompt, client, model):
    therapist_messages = [
        {"role": "system", "content": therapist_prompt},
        {"role": "user", "content": "(Start)"}
    ]

    child_messages = [
        {"role": "system", "content": child_prompt},
    ]

    while True:
        owlbot_response = client.chat.completions.create(
            model=model,
            messages=therapist_messages,
            max_tokens=500,
            temperature=1,
        )

        print(f'OwlBot: {owlbot_response.choices[0].message.content}')
        therapist_messages.append({"role": "assistant", "content": owlbot_response.choices[0].message.content})
        child_messages.append({"role": "user", "content": owlbot_response.choices[0].message.content})

        child_response = client.chat.completions.create(
            model=model,
            messages=child_messages,
            max_tokens=500,
            temperature=1,
        )

        print(f'Child: {child_response.choices[0].message.content}')
        if "(FLAG: STOP)" in child_response.choices[0].message.content:
            print('Session ended.')
            break

        therapist_messages.append({"role": "user", "content": child_response.choices[0].message.content})
        child_messages.append({"role": "assistant", "content": child_response.choices[0].message.content})


for client, model in [(deepseek_client, "deepseek-chat"), (gpt_client, "gpt-4o-mini-2024-07-18")]:
    print(f"Using {model}")
    simulate(therapist_prompt, child_prompt, client, model)
    print('='*50)
