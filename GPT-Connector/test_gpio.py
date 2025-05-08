import RPi.GPIO as GPIO
import time

BUTTON_PIN = 2  # BCM numbering
LED_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

print("Press the button to turn on the LED. Ctrl+C to exit.")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button pressed
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("Button pressed! LED ON")
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting test.")
finally:
    GPIO.cleanup()