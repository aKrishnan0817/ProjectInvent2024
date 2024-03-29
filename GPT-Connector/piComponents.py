import time
try:
    from gpiozero import Button
    import RPi.GPIO as GPIO
except:
    print("")

class piComponenets:
    #button is 2 and led is 4
    def __init__(self, buttonPin, ledPin):
        self.buttonPin = buttonPin
        self.ledPin = ledPin
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(ledPin,GPIO.OUT)
            button = Button(4)
            self.buttonUse=True
        except:
            self.buttonUse= False

    def checkButtonPress():
        if self.buttonUse:
            while True:
                if button.is_pressed:
                    setLed(1)
                    time.sleep(1)
                    setLed(0)
                    return True

                else:
                    setLed(0)
        return None

    #0 for off - 1 for on
    def setLed(onOff):
        if onOff:
            GPIO.output(self.ledPin,GPIO.HIGH)
        GPIO.output(self.ledPin,GPIO.LOW)

    def getButtonUse():
        return self.buttonUse
