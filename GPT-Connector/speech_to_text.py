import speech_recognition as sr

buttonUse = True
try:
    from gpiozero import Button
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4,GPIO.OUT)
    button = Button(2)
except:
    buttonUse= False

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        if buttonUse:
            while True:
                if button.is_pressed:
                    print("Listening")
                    GPIO.output(4,GPIO.HIGH)
                    try:
                        audio = recognizer.listen(source, timeout=10)# Record audio for up to 10 seconds
                        break
                    except:
                        print("coudlnt listen")
                else:
                    GPIO.output(4,GPIO.LOW)
                    #break
        else:
            audio = recognizer.listen(source, timeout=10)

    try:
        print("Transcribing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Error connecting to Google API: {e}")
