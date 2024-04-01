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
            GPIO.setup(self.ledPin,GPIO.OUT)
            self.button = Button(self.buttonPin)
            self.buttonUse=True
        except:
            self.buttonUse= False

    def checkButtonPress(self):
        if self.buttonUse:
            while True:
                if self.button.is_pressed:
                    setLed(1)
                    time.sleep(1)
                    setLed(0)
                    return True

                else:
                    setLed(0)
        return None

    #0 for off - 1 for on
    def setLed(self,onOff):
        if self.buttonUse:
            GPIO.setup(self.ledPin,GPIO.OUT)
            if onOff:
                GPIO.output(self.ledPin,GPIO.HIGH)
            GPIO.output(self.ledPin,GPIO.LOW)

    def getButtonUse(self):
        return self.buttonUse
