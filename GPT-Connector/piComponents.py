import time

try:
    from gpiozero import Button
    import RPi.GPIO as GPIO
except:
    print("Failed to import gpiozero or RPi.GPIO. This likely means you're running on a non-Raspberry Pi environment.")
    import traceback
    traceback.print_exc()


class piComponents:
    # button is 2 and led is 4
    def __init__(self, buttonPin, ledPin):
        self.buttonPin = buttonPin
        self.ledPin = ledPin
        print(f"[piComponents] Initialized with buttonPin={self.buttonPin}, ledPin={self.ledPin}")
        try:
            print("[piComponents] GPIO.cleanup() called to reset any previous configuration")
            GPIO.cleanup()
            print("[piComponents] GPIO mode set to BCM")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.ledPin, GPIO.OUT)
            print(f"[piComponents] LED pin {self.ledPin} set as OUTPUT")
            print(f"[piComponents] Attempting to initialize Button on GPIO pin {self.buttonPin}")
            self.button = Button(self.buttonPin)
            print("[piComponents] Button initialized successfully. Button will be used.")
            self.buttonUse = True
        except:
            print("[piComponents][ERROR] Exception during GPIO/Button initialization. This may mean you're not running on a Raspberry Pi or the GPIO pins are already in use.")
            import traceback
            traceback.print_exc()
            print("[piComponents][ERROR] Tip: r conflicting uses of the GPIO pin. You can also call GPIO.cleanup() before setup.")

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