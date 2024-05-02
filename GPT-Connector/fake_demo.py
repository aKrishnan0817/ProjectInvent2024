from TTS import ttsPlay

responses=["What game would you like to play? We can play 20 questions, Superhero Trivia or geography trivia.",
" Sure, let's start. Here's your first question: What is the real name of Wonder Woman in the comics?",
"Correct! Well done. Now let's go to the next question:"]

for x in responses:
    waitForEnter = input("Press enter to go to next responses.")
    ttsPlay(x)
