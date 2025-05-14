import time

try:
    from gpiozero import Button
    import RPi.GPIO as GPIO
except:
    print("")


class piComponents:
    # button is 2 and led is 4
    def __init__(self, buttonPin, ledPin):
        self.buttonPin = buttonPin
        self.ledPin = ledPin
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.ledPin, GPIO.OUT)
            self.button = Button(self.buttonPin)
            self.buttonUse = True
        except:
            self.buttonUse = False

    def checkButtonPress(self):
        if self.buttonUse:
            while True:
                if self.button.is_pressed:
                    self.setLed(1)
                    time.sleep(1)
                    self.setLed(0)
                    return True

                else:
                    self.setLed(0)
        return None

    # 0 for off - 1 for on
    def setLed(self, onOff):
        if self.buttonUse:
            GPIO.setup(self.ledPin, GPIO.OUT)
            if onOff:
                GPIO.output(self.ledPin, GPIO.HIGH)
                print("turning led on")
            GPIO.output(self.ledPin, GPIO.LOW)

    def getButtonUse(self):
        return self.buttonUse

if __name__ == "__main__":
    button = piComponents(buttonPin=2, ledPin=4)
    print(button.checkButtonPress())
    print(button.getButtonUse())
    button.setLed(1)
    time.sleep(1)
    button.setLed(0)
    GPIO.cleanup()