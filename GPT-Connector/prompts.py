promptList =[0]
latestVersion =2 #LATEST VERSION IS HERE
print("Enter which version you'd like to use (1,2,3,4..)")
version = int(input(""))
while version not in list(range(latestVersion+1)):
    print("Enter an integer value between 1 and ",latestVersion)

"""

To use a new prompt go to an empty version(where it says distress="" and coping= "")
and write a prompt between the quotations marks. Afterwards when running the code it will ask
you what version you'd like to use and simply type the version you have recently modified.

Afterwars a increment latestVersion to the version you have recently worked on.
"""



distressPrompt="notify caregivers that user is distressed only if the user explicity mentions distress"
copingPrompt="the user would like to practice coping skills such as meditation or breathing excerises"
V1={"distressPrompt":distressPrompt,"copingPrompt":copingPrompt}
promptList.append(V1)


distressPrompt='the user explicitly states that they are in a state of distress and uses the word "distress"'
copingPrompt="the user would like to practice coping skills such as meditation or breathing excerises"
V2={"distressPrompt":distressPrompt,"copingPrompt":copingPrompt}
promptList.append(V2)


distressPrompt=""
copingPrompt=""
V3={"distressPrompt":distressPrompt,"copingPrompt":copingPrompt}
promptList.append(V3)


distressPrompt=""
copingPrompt=""
V4={"distressPrompt":distressPrompt,"copingPrompt":copingPrompt}
promptList.append(V4)


distressPrompt=""
copingPrompt=""
V5={"distressPrompt":distressPrompt,"copingPrompt":copingPrompt}
promptList.append(V5)
