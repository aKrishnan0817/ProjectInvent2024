import time

try:
    from gpiozero import Button
    import RPi.GPIO as GPIO
    from gpiozero.pins.lgpio import LGPIOFactory

    Button.pin_factory = LGPIOFactory()  # force gpiozero to use lgpio
except Exception as e:
    print("GPIO libraries not available. Running in non-GPIO mode. Error:", e)


class piComponents:
    # button is 2 and led is 4
    def __init__(self, buttonPin, ledPin):
        self.buttonPin = buttonPin
        self.ledPin = ledPin
        print("1. Check that we're connected to Raspberry PI and not computer")
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.ledPin, GPIO.OUT, initial=GPIO.LOW)
            # pull-up + 50 ms debounce
            self.button = Button(self.buttonPin, pull_up=True, bounce_time=0.05)
            self.buttonUse = True
            print("Button initialized on pin", self.buttonPin)
            print("LED initialized on pin", self.ledPin)
        except Exception as e:
            print("Error initializing GPIO:", e)
            self.buttonUse = False

    def checkButtonPress(self):
        if self.buttonUse:
            if self.button.is_pressed:
                print("3. Button pressed")
                self.setLed(1)
                return True
            else:
                self.setLed(0)
        return False

    def isButtonPressed(self):
        return self.button.is_pressed if self.buttonUse else False

    # 0 for off - 1 for on
    def setLed(self, onOff):
        if self.buttonUse:
            GPIO.output(self.ledPin, GPIO.HIGH if onOff else GPIO.LOW)
            print("turning led on" if onOff else "turning led off")

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