import time
import RPi.GPIO as GPIO

class piComponents:
    def __init__(self, buttonPin, ledPin):
        self.buttonPin = buttonPin
        self.ledPin = ledPin
        print(f"[piComponents] Initializing with buttonPin={self.buttonPin}, ledPin={self.ledPin}")
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.ledPin, GPIO.OUT)
            print("[piComponents] GPIO setup successful.")
            self.buttonUse = True
        except Exception as e:
            print("[piComponents][ERROR] Failed to initialize GPIO.")
            import traceback
            traceback.print_exc()
            self.buttonUse = False

    def checkButtonPress(self):
        if self.buttonUse:
            while True:
                if GPIO.input(self.buttonPin) == GPIO.LOW:
                    self.setLed(1)
                    print("[piComponents] Button pressed!")
                    time.sleep(1)
                    self.setLed(0)
                    return True
                else:
                    self.setLed(0)
        return None

    def setLed(self, onOff):
        if self.buttonUse:
            GPIO.setup(self.ledPin, GPIO.OUT)
            if onOff:
                GPIO.output(self.ledPin, GPIO.HIGH)
                print("[piComponents] LED ON")
            else:
                GPIO.output(self.ledPin, GPIO.LOW)
                print("[piComponents] LED OFF")

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